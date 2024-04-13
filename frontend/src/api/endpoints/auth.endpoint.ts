import { AuthDto } from "api/models/auth.model";
import api from "api/utils/api";
import { setStoredAuthToken } from "api/utils/authToken";
import { parseJwt } from "api/utils/parseJwt";

export namespace AuthEndpoint {
  export const login = async (username: string, password: string) => {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    const result = await api.post<AuthDto.Result>("/auth/login", params.toString(), {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    });

    setStoredAuthToken(result.access_token);
    return parseJwt<AuthDto.Item>(result.access_token);
  };

  export const loginVk = async (code: string) => {
    const result = await api.post<AuthDto.Result>(`/auth/vk?code=${code}`);

    setStoredAuthToken(result.access_token);
    return parseJwt<AuthDto.Item>(result.access_token);
  };

  export const register = async (email: string, username: string, password: string) => {
    const result = await api.post<AuthDto.Result>("/auth/register", {
      email,
      first_name: username,
      last_name: "",
      password
    });

    setStoredAuthToken(result.access_token);
    return parseJwt<AuthDto.Item>(result.access_token);
  };
}
