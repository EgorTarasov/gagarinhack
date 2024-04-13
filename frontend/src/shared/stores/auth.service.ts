import { AuthEndpoint } from "api/endpoints/auth.endpoint";
import { UserEndpoint } from "api/endpoints/user.endpoint";
import { AuthDto } from "api/models/auth.model";
import { UserDto } from "api/models/user.model";
import { removeStoredAuthToken } from "api/utils/authToken";
import { makeAutoObservable } from "mobx";
import { TUser } from "react-telegram-auth";

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
    this.auth = {
      state: "authorized",
      user: {
        adaptation_target: "",
        email: "",
        first_name: "",
        id: 0,
        last_name: "",
        number: "",
        position: { id: 0, name: "" },
        position_id: 0,
        starts_work_at: ""
      }
    };
    return;
    // try {
    //   const user = await UserEndpoint.current();
    //   this.auth = {
    //     state: "authorized",
    //     user
    //   };
    // } catch {
    //   this.auth = { state: "anonymous" };
    // }
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
        return true;
      }
    } catch {
      this.auth = { state: "anonymous" };
    }
    return false;
  }

  async logout() {
    this.auth = { state: "anonymous" };
    removeStoredAuthToken();
  }
}

export const AuthService = new AuthServiceViewModel();
