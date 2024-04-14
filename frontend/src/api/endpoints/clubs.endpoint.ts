import api from "api/utils/api";

export interface ClubResult {
  title: string;
  description: string;
  contact: string;
}

export const getClubs = async () => {
  const res = await api.get("/clubs/");

  return res as ClubResult[];
};
