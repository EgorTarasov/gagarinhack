import { AuthEndpoint } from "api/endpoints/auth.endpoint";
import { UserEndpoint } from "api/endpoints/user.endpoint";
import { UserDto } from "api/models/user.model";
import { removeStoredAuthToken } from "api/utils/authToken";
import { makeAutoObservable } from "mobx";
import { MainPageStore } from "../../pages/main/main.vm";
import { AchievementEndpoint } from "api/endpoints/achievement.endpoint";

export type Auth =
  | {
      state: "loading";
    }
  | {
      state: "anonymous";
    }
  | {
      state: "authorized";
      user: UserDto.Item;
    };

class AuthServiceViewModel {
  public auth: Auth = { state: "loading" };

  constructor() {
    makeAutoObservable(this);
    void this.init();
  }

  private async init() {
    try {
      const user = await UserEndpoint.current();
      this.auth = {
        state: "authorized",
        user
      };
      if (!MainPageStore.achievements.length) {
        MainPageStore.achievements = await AchievementEndpoint.current(user.id.toString());
      }
    } catch {
      this.auth = { state: "anonymous" };
    }
  }

  public async login(username: string, password: string): Promise<boolean> {
    if (!username || !password) return false;
    try {
      const auth = await AuthEndpoint.login(username, password);
      if (auth) {
        const user = await UserEndpoint.current();
        this.auth = {
          state: "authorized",
          user
        };
        if (!MainPageStore.achievements.length) {
          MainPageStore.achievements = await AchievementEndpoint.current(user.id.toString());
        }
        return true;
      }
    } catch {
      this.auth = { state: "anonymous" };
    }
    return false;
  }

  public async loginVk(code: string): Promise<boolean> {
    try {
      const auth = await AuthEndpoint.loginVk(code);
      if (auth) {
        const user = await UserEndpoint.current();
        this.auth = {
          state: "authorized",
          user
        };
        if (!MainPageStore.achievements.length) {
          MainPageStore.achievements = await AchievementEndpoint.current(user.id.toString());
        }
        return true;
      }
    } catch {
      this.auth = { state: "anonymous" };
    }
    return false;
  }

  public register = async (email: string, name: string, password: string): Promise<boolean> => {
    try {
      const auth = await AuthEndpoint.register(email, name, password);
      if (auth) {
        const user = await UserEndpoint.current();
        this.auth = {
          state: "authorized",
          user
        };
        if (!MainPageStore.achievements.length) {
          MainPageStore.achievements = await AchievementEndpoint.current(user.id.toString());
        }
        return true;
      }
    } catch {
      this.auth = { state: "anonymous" };
    }
    return false;
  };

  async logout() {
    this.auth = { state: "anonymous" };
    removeStoredAuthToken();
  }
}

export const AuthService = new AuthServiceViewModel();
