import { ComponentType } from "react";
import { NewsPage } from "../pages/events/news.page.tsx";
import { TasksPage } from "../pages/tasks/tasks.page.tsx";
import { ContactsPage } from "../pages/staff/staff.page.tsx";
import { PrivateRoute } from "@/hoc/PrivateRoute.tsx";
import { AuthService } from "@/stores/auth.service.ts";
import { makeAutoObservable } from "mobx";
import { MainPage } from "../pages/main/main.page.tsx";
import { Login } from "../pages/login/Login.tsx";
import { ResetPassword } from "../pages/reset-password/ResetPassword.tsx";
import { AssistantPage } from "../pages/assistant/assistant.page.tsx";
import { AttendancePage } from "../pages/admin/attendance/attendance.page.tsx";

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
    path: "/news",
    component: () => (
      <PrivateRoute>
        <NewsPage />
      </PrivateRoute>
    ),
    title: "Новости",
    showInNav: true
  },
  {
    path: "/contacts",
    component: () => (
      <PrivateRoute>
        <ContactsPage />
      </PrivateRoute>
    ),
    title: "Контакты",
    showInNav: true
  }
];

const adminRoutes: RouteType[] = [
  {
    path: "/attendance",
    component: () => (
      <PrivateRoute>
        <AttendancePage />
      </PrivateRoute>
    ),
    title: "Посещаемость",
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
      return [...globalRoutes, ...userRoutes, ...adminRoutes];
    }
    return globalRoutes;
  }
}

export const RoutesStore = new routesStore();
