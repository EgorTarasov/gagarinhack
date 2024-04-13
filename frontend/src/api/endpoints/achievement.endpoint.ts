import { AchievementDto } from "api/models/achievement.model";
import api from "api/utils/api";

export namespace AchievementEndpoint {
  export const current = async (user_id: string) => {
    const res = await api.get(`/achievements/get?user_id=${user_id}`);
    return res as AchievementDto.Item[];
  };

  export const create = async (item: AchievementDto.Template) => {
    const formData = new FormData();
    formData.append("user_id", item.user_id.toString());
    formData.append("title", item.title);
    formData.append("date", item.date);
    formData.append("place", item.place);
    formData.append("description", item.description);
    formData.append("type", item.type);
    formData.append("event_link", item.event_link);
    formData.append("file", item.file);
    const res = await api.post("/achievements/upload", formData);
    return res as AchievementDto.Item;
  };
}
