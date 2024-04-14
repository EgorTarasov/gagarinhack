import { ClubResult, getClubs } from "api/endpoints/clubs.endpoint";
import { NewsEndpoint } from "api/endpoints/news.endpoint";
import { AchievementDto } from "api/models/achievement.model";
import { NewsDto } from "api/models/news.model";
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
  }

  async init() {
    const [newsRes] = await Promise.all([NewsEndpoint.current()]);
    this.news = newsRes;
    this.clubs = await getClubs();
    this.isLoading = false;
  }
}

export const MainPageStore = new MainPageViewModel();
