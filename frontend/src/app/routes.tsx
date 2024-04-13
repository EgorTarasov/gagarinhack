import { ComponentType } from "react";
import { ProfilePage } from "../pages/profile/profile.page.tsx";
import { EventsPage } from "../pages/events/events.page.tsx";
import { EducationPage } from "../pages/education/education.page.tsx";
import { TasksPage } from "../pages/tasks/tasks.page.tsx";
import { StaffPage } from "../pages/staff/staff.page.tsx";
import { PrivateRoute } from "@/hoc/PrivateRoute.tsx";
import { AuthService } from "@/stores/auth.service.ts";
import { makeAutoObservable } from "mobx";
import { OnboardingPage } from "../pages/onboarding/onboarding.page.tsx";
import { MainPage } from "../pages/main/main.page.tsx";
import { Login } from "../pages/login/Login.tsx";
import { ResetPassword } from "../pages/reset-password/ResetPassword.tsx";
import { AssistantPage } from "../pages/assistant/assistant.page.tsx";

export interface RouteType {
  path: string;
  component: ComponentType;
  title: string;
  showInNav?: boolean;
}

export const RoutesWithoutNav = ["/login", "/reset-password"];

const userRoutes: RouteType[] = [
  {
    path: "/",
    component: () => (
      <PrivateRoute>
        <MainPage />
      </PrivateRoute>
    ),
    title: "Главная",
    showInNav: true
  },
  {
    path: "/assistant",
    component: () => (
      <PrivateRoute>
        <AssistantPage />
      </PrivateRoute>
    ),
    title: "Ассистент"
  },
  {
    path: "/me",
    component: () => (
      <PrivateRoute>
        <ProfilePage />
      </PrivateRoute>
    ),
    title: "Профиль"
  },
  {
    path: "/onboarding",
    component: () => (
      <PrivateRoute>
        <OnboardingPage />
      </PrivateRoute>
    ),
    title: "Онбординг",
    showInNav: true
  },
  {
    path: "/education",
    component: () => (
      <PrivateRoute>
        <EducationPage />
      </PrivateRoute>
    ),
    title: "Обучение",
    showInNav: true
  },
  {
    path: "/education/:id",
    component: () => (
      <PrivateRoute>
        <EducationPage />
      </PrivateRoute>
    ),
    title: "Обучение",
    showInNav: false
  },
  {
    path: "/education/:id/task/:taskId",
    component: () => (
      <PrivateRoute>
        <EducationPage />
      </PrivateRoute>
    ),
    title: "Обучение",
    showInNav: false
  },
  {
    path: "/tasks",
    component: () => (
      <PrivateRoute>
        <TasksPage />
      </PrivateRoute>
    ),
    title: "Задания",
    showInNav: true
  },
  {
    path: "/tasks/:id",
    component: () => (
      <PrivateRoute>
        <TasksPage />
      </PrivateRoute>
    ),
    title: "Задания"
  },
  {
    path: "/events",
    component: () => (
      <PrivateRoute>
        <EventsPage />
      </PrivateRoute>
    ),
    title: "Мероприятия",
    showInNav: true
  },
  {
    path: "/events/:id",
    component: () => (
      <PrivateRoute>
        <EventsPage />
      </PrivateRoute>
    ),
    title: "Мероприятия",
    showInNav: false
  },
  {
    path: "/contacts",
    component: () => (
      <PrivateRoute>
        <StaffPage />
      </PrivateRoute>
    ),
    title: "Контакты",
    showInNav: true
  }
];

export const globalRoutes: RouteType[] = [
  {
    path: "/login",
    component: () => <Login />,
    title: "Вход"
  },
  {
    path: "/reset-password",
    component: () => <ResetPassword />,
    title: "Восстановление пароля"
  }
];

class routesStore {
  constructor() {
    makeAutoObservable(this);
  }

  get routes() {
    if (AuthService.auth.state === "authorized") {
      return [...globalRoutes, ...userRoutes];
    }
    return globalRoutes;
  }
}

export const RoutesStore = new routesStore();
