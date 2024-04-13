import { Button, Logo } from "@/ui";
import { Input } from "@/ui/Input";
import { FormEvent, useEffect, useState } from "react";
import { AuthService } from "@/stores/auth.service.ts";
import { AuthDto } from "api/models/auth.model.ts";
import { Link, useNavigate } from "react-router-dom";
import { observer } from "mobx-react-lite";
import { MOCK_HR, MOCK_USER } from "@/constants/mocks";
import { PasswordField } from "@/components/fields/PasswordField";
import { VKButton } from "@/components/buttons/VkLoginButton";

export const Login = observer(() => {
  const navigate = useNavigate();
  const [showError, setShowError] = useState<boolean>(false);
  const [authData, setAuthData] = useState<AuthDto.Login>(MOCK_USER);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoginView, setIsLoginView] = useState(true);
  const [repeatPassword, setRepeatPassword] = useState("");
  const [name, setName] = useState("");
  const [showTestHr, setShowTestHr] = useState(false);

  const handleFormSubmit = async (e: FormEvent) => {
    e.preventDefault();

    setIsLoading(true);
    setShowError(false);
    try {
      if (isLoginView) {
        const isSuccess = await AuthService.login(authData.username, authData.password);
        if (isSuccess) {
          navigate("/");
        } else {
          setShowError(true);
        }
      } else {
        if (authData.password !== repeatPassword) {
          setShowError(true);
          return;
        }
        const isSuccess = await AuthService.register(authData.username, name, authData.password);
        if (isSuccess) {
          navigate("/");
        } else {
          setShowError(true);
        }
      }
      return;
    } catch {
      setShowError(true);
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
    if (showTestHr) {
      setAuthData(MOCK_USER);
    } else {
      setAuthData(MOCK_HR);
    }
    setShowTestHr((v) => !v);
  };

  useEffect(() => {
    const vkLoginCode = new URLSearchParams(window.location.search).get("code");
    if (vkLoginCode) {
      setIsLoading(true);
      AuthService.loginVk(vkLoginCode).then((isSuccess) => {
        if (isSuccess) {
          navigate("/");
        }
        setIsLoading(false);
      });
    }
  }, [navigate]);

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
            label={"Почта"}
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
          {!isLoginView && (
            <Input
              disabled={isLoading}
              label={"Имя"}
              type="text"
              required
              aria-label={"Имя"}
              autoComplete={"name"}
              name={"name"}
              value={name}
              error={showError}
              placeholder={"Введите имя"}
              onChange={setName}
            />
          )}
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
            <div className="h-1"></div>
            {!isLoginView && (
              <PasswordField
                disabled={isLoading}
                label={"Повторите пароль"}
                required
                autoComplete={"repeat-password"}
                name={"repeat-password"}
                value={repeatPassword}
                error={showError}
                aria-label={"Повторите Пароль"}
                placeholder={"Введите пароль повторно"}
                onChange={setRepeatPassword}
              />
            )}
            <div className={"flex items-center"}>
              {isLoginView && (
                <Link
                  to="/reset-password"
                  className={
                    "text-text-primary/60 text-sm hover:text-text-primary transition-colors duration-200"
                  }>
                  Забыли пароль?
                </Link>
              )}
              <div className="flex-1"></div>
              <button
                type="button"
                className="text-text-primary/60 text-sm hover:text-text-primary transition-colors duration-200"
                onClick={() => setIsLoginView((v) => !v)}>
                {!isLoginView ? "Войти" : "Регистрация"}
              </button>
            </div>
          </div>
          {showError && (
            <span className={"text-center text-error text-sm"}>
              {isLoginView ? "Неверный логин или пароль" : "Проверьте все поля"}
            </span>
          )}
          <Button disabled={isLoading} type="submit" className="mt-4">
            {isLoginView ? "Войти" : "Регистрация"}
          </Button>
          <VKButton />
          <button
            type="button"
            className="text-text-primary/60 text-sm hover:text-text-primary transition-colors duration-200 underline hover:no-underline"
            onClick={fillTestData}>
            Тестовый {showTestHr ? "юзер" : "админ"}
          </button>
        </form>
        <div className="h-4" />
      </div>
    </div>
  );
});
