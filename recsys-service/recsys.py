import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from psycopg2 import connect
from clickhouse_driver import Client
from transformers import AutoTokenizer, AutoModel
import torch
import logging


log = logging.getLogger("recsys")


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
        self.pg_conn = connect(**db_params)

        self.ch_params = ch_params
        self.ch_client = Client(**ch_params)
        self.model.eval()

    def get_embeddings(self, text):
        test_batch = self.tokenizer.batch_encode_plus(
            text, return_tensors="pt", padding=True
        )
        with torch.no_grad():
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

    # def find_similar_news(self, embedding, client):
    #     # Convert the embedding to a string of comma-separated values
    #     embedding_str = ",".join(map(str, embedding))

    #     # Write a query that calculates the cosine similarity
    #     query = f"""
    #     SELECT title, dotProduct(embedding, [{embedding_str}]) / (sqrt(dotProduct(embedding, embedding)) * sqrt(dotProduct([{embedding_str}], [{embedding_str}]))) as similarity
    #     FROM news_embeddings
    #     ORDER BY similarity DESC
    #     LIMIT 2
    #     """

    #     # Execute the query
    #     result = client.execute(query)

    #     # The result is already sorted by similarity, so we can return it directly
    #     return result

    def main(self, vk_group_ids) -> list[tuple[str, float]]:

        all_embeddings = []
        start = time.time()
        log.info("starting calculatin embedings")
        cnt = 0
        with self.pg_conn.cursor() as cursor:
            ep_start = time.time()
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
            cnt += 1
            log.info(
                f"calculated for {cnt}/ {len(vk_group_ids)} in {time.time() - ep_start}"
            )

        log.info(f"calculated in {time.time() - start}")
        # Усредняем эмбеддинги
        start2 = time.time()
        mean_embedding = np.mean(all_embeddings, axis=0)

        # Ищем похожие новости
        similar_news = self.find_similar_news(mean_embedding, self.ch_client)
        log.info(f"found closest in {time.time() - start2}")
        return similar_news
