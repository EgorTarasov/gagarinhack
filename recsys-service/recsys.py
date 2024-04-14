import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from psycopg2 import connect
from clickhouse_driver import Client
from transformers import AutoTokenizer, AutoModel
import torch


class Recsys:
    def __init__(self, model_name: str, db_params: dict, ch_params: dict):
        self.model = AutoModel.from_pretrained(
            pretrained_model_name_or_path=model_name,
            # trust_remote_code=True,
            # attn_implementation="eager",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=model_name
        )
        self.db_params = db_params
        self.ch_params = ch_params

    def get_embeddings(self, text):
        test_batch = self.tokenizer.batch_encode_plus(
            text, return_tensors="pt", padding=True
        )
        with torch.inference_mode():
            pooled_output = self.model(**test_batch).pooler_output
        return pooled_output

    def find_similar_news(self, embedding, client):
        query = "SELECT title, embedding FROM news_embeddings"
        result = client.execute(query)
        titles = []
        embeddings = []
        for row in result:
            titles.append(row[0])
            embeddings.append(row[1])

        similarities = cosine_similarity(embedding, embeddings)[0]
        top_two_idx = np.argsort(similarities)[-2:]
        return [(titles[i], similarities[i]) for i in top_two_idx][::-1]

    def main(self, vk_group_ids) -> list[tuple[str, float]]:
        conn = connect(**self.db_params)
        ch_client = Client(**self.ch_params)
        all_embeddings = []

        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT name, description FROM vk_groups WHERE id = ANY(%s)",
                (vk_group_ids,),
            )
            rows = cursor.fetchall()

            if not rows:
                raise ValueError("No groups found")

            texts = [f"{row[0]}[SEP]{row[1]}" for row in rows]
            embeddings = self.get_embeddings(texts)
            embeddings = embeddings.detach().numpy()
            all_embeddings.append(embeddings)

        # Усредняем эмбеддинги

        mean_embedding = np.mean(all_embeddings, axis=0)

        # Ищем похожие новости
        similar_news = self.find_similar_news(mean_embedding, ch_client)

        conn.close()

        return similar_news
