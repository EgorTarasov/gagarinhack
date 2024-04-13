import { NewsDto } from "api/models/news.model";
import api from "api/utils/api";

export namespace NewsEndpoint {
  export const current = async (): Promise<NewsDto.Item[]> => {
    const data = await api.get<NewsDto.Result[]>("/news/?offset=0&limit=35");
    return data.map(NewsDto.convertDto);
  };
}
