import { Button, Logo } from "@/ui";
import { Input } from "@/ui/Input";
import { FormEvent, useState } from "react";
import { AuthService } from "@/stores/auth.service.ts";
import { AuthDto } from "api/models/auth.model.ts";
import { Link, useNavigate } from "react-router-dom";
import { observer } from "mobx-react-lite";
import { MOCK_USER } from "@/constants/mocks";
import { PasswordField } from "@/components/fields/PasswordField";
import { TLoginButton, TLoginButtonSize, TUser } from "react-telegram-auth";

export const Login = observer(() => {
  const navigate = useNavigate();
  const [showError, setShowError] = useState<boolean>(false);
  const [authData, setAuthData] = useState<AuthDto.Login>(MOCK_USER);
  const [isLoading, setIsLoading] = useState(false);

  const handleFormSubmit = async (e: FormEvent) => {
    e.preventDefault();

    setIsLoading(true);
    setShowError(false);
    try {
      const isSuccess = await AuthService.login(authData.username, authData.password);
      if (isSuccess) {
        navigate("/");
      } else {
        setShowError(true);
      }
    } catch {
      setShowError(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTelegramLogin = async (user: TUser) => {
    setIsLoading(true);
    setShowError(false);
    try {
      const isSuccess = await AuthService.loginWithTelegram(user);
      if (isSuccess) {
        navigate("/");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handlePasswordChange = (value: string) => {
    setAuthData({ ...authData, password: value });
  };

  const handleUsernameChange = (value: string) => {
    setAuthData({ ...authData, username: value });
  };

  const fillTestData = () => {
    setAuthData(MOCK_USER);
  };

  return (
    <div className={"w-full h-full flex items-center justify-center bg-white"}>
      <div className={"max-w-[320px] w-full p-5 flex flex-col items-center"}>
        <div className={"mb-5 w-full flex items-center justify-center"}>
          <Logo />
        </div>
        <form
          onSubmit={handleFormSubmit}
          aria-label="Два поля: почта и пароль, либо вход через Telegram"
          className={"flex flex-col gap-3 w-full"}>
          <Input
            disabled={isLoading}
            label={"Логин"}
            type="email"
            required
            aria-label={"Почта"}
            autoComplete={"email"}
            name={"email"}
            value={authData.username}
            error={showError}
            placeholder={"Введите почту"}
            onChange={handleUsernameChange}
          />
          <div className={"flex flex-col flex-end gap-1"}>
            <PasswordField
              disabled={isLoading}
              label={"Пароль"}
              required
              autoComplete={"current-password"}
              name={"password"}
              value={authData.password}
              error={showError}
              aria-label={"Пароль"}
              placeholder={"Введите пароль"}
              onChange={handlePasswordChange}
            />
            <div className={"flex items-center justify-between"}>
              <Link
                to="/reset-password"
                className={
                  "text-text-primary/60 text-sm hover:text-text-primary transition-colors duration-200"
                }>
                Забыли пароль?
              </Link>
              {(authData.username !== MOCK_USER.username ||
                authData.password !== MOCK_USER.password) && (
                <button
                  type="button"
                  className="text-text-primary/60 text-sm hover:text-text-primary transition-colors duration-200 underline hover:no-underline"
                  onClick={fillTestData}>
                  Тестовый юзер
                </button>
              )}
            </div>
          </div>
          {showError && (
            <span className={"text-center text-error text-sm"}>Неверный логин или пароль</span>
          )}
          <Button disabled={isLoading} type="submit" className="mt-4">
            Войти
          </Button>
        </form>
        <div className="h-4" />
        <TLoginButton
          botName="discrete_third_bot"
          buttonSize={TLoginButtonSize.Large}
          lang="ru"
          usePic={false}
          cornerRadius={8}
          requestAccess="write"
          onAuthCallback={handleTelegramLogin}
        />
      </div>
    </div>
  );
});
