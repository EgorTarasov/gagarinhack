import { AuthService } from "@/stores/auth.service";
import { AchievementEndpoint } from "api/endpoints/achievement.endpoint";
import { NewsEndpoint } from "api/endpoints/news.endpoint";
import { AchievementDto } from "api/models/achievement.model";
import { NewsDto } from "api/models/news.model";
import { autorun, makeAutoObservable } from "mobx";

export class MainPageViewModel {
  news: NewsDto.Item[] = [];
  achievements: AchievementDto.Item[] = [];
  public isLoading = false;

  constructor() {
    makeAutoObservable(this);
    void this.init();

    autorun(() => {
      if (AuthService.auth.state === "authorized") {
        AchievementEndpoint.current(AuthService.auth.user.id.toString()).then((res) => {
          this.achievements = res;
        });
      }
    });
  }

  private async init() {
    const [newsRes] = await Promise.all([NewsEndpoint.current()]);
    this.news = newsRes;
    console.log(newsRes);
    this.isLoading = false;
  }
}

export const MainPageStore = new MainPageViewModel();
