import api from "api/utils/api";

export const getClubs = async () => {
  const res = await api.get("/clubs/");

  return res;
};
