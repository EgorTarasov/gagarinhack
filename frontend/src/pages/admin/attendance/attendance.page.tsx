import { observer } from "mobx-react-lite";
import { useRef, useState } from "react";
import LandscapeIcon from "./assets/landscape.svg";
import { AttendanceViewModel } from "./attendance.vm";
import { Input } from "@/ui";
import { twMerge } from "tailwind-merge";

export const AttendancePage = observer(() => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [vm] = useState(() => new AttendanceViewModel());

  return (
    <div className="flex w-full py-6 px-4 flex-col gap-4 mx-auto max-w-screen-desktop overflow-hidden">
      <h1 className="text-4xl font-semibold">Проверка посещаемости</h1>
      <div className="flex gap-4 pt-6">
        <div className="flex-1 px-10 py-7 rounded-2xl bg-white flex flex-col gap-8">
          <h2 className="text-2xl font-medium">Фото аудитории</h2>
          <p>
            Загрузите фотографию/фотографии аудитории, важно,
            <br /> чтобы на снимке было видно всех студентов.
          </p>
          <form
            onSubmit={(e) => {
              e.preventDefault();
            }}
            className={twMerge(
              "relative w-full border border-primary border-dashed rounded-2xl flex flex-col items-center justify-center gap-3 py-5",
              vm.loading && "opacity-50"
            )}>
            <input
              ref={inputRef}
              disabled={vm.loading}
              type="file"
              name="file"
              accept="image/*"
              className={twMerge(
                "absolute h-full w-full opacity-0",
                !vm.loading && "cursor-pointer"
              )}
              multiple
              onChange={(e) => e.target.files && vm.onRequest(Array.from(e.target.files))}
            />
            <LandscapeIcon />
            <p className="text-text-primary text-lg">Перетащите фотографии сюда</p>
            <span>или</span>
            <button
              type="button"
              className="bg-primary text-white px-6 py-2 rounded-lg"
              onClick={() => inputRef.current?.click()}>
              Выберите файл
            </button>
          </form>
        </div>
        <div className="flex-1 flex flex-col">
          <div className="w-fit">
            <Input disabled={vm.loading} label="Укажите номер группы" placeholder="ИТ-24" />
          </div>
        </div>
      </div>
    </div>
  );
});
