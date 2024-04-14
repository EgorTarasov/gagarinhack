import { ClubResult, getClubs } from "api/endpoints/clubs.endpoint";
import { NewsEndpoint } from "api/endpoints/news.endpoint";
import { AchievementDto } from "api/models/achievement.model";
import { NewsDto } from "api/models/news.model";
import api from "api/utils/api";
import { getStoredAuthToken } from "api/utils/authToken";
import { makeAutoObservable } from "mobx";

export class MainPageViewModel {
  news: NewsDto.Item[] = [];
  clubs: ClubResult[] = [];
  achievements: AchievementDto.Item[] = [];
  selectedAchievement: AchievementDto.Item | null = null;
  public isLoading = false;

  constructor() {
    makeAutoObservable(this);
    void this.init();
  }

  async downloadCertificate() {
    if (!this.selectedAchievement) return;

    const res = await fetch(
      `${import.meta.env.VITE_API_URL}/achievements/download?file_link=${
        this.selectedAchievement.file_link
      }`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getStoredAuthToken()}`
        }
      }
    );
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "certificate.pdf";
    document.body.appendChild(a);
    a.click();
  }

  async init() {
    const [newsRes] = await Promise.all([NewsEndpoint.current()]);
    this.news = newsRes;
    this.clubs = await getClubs();
    this.isLoading = false;
  }
}

export const MainPageStore = new MainPageViewModel();
