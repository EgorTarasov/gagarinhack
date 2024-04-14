import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../../main.vm";
import { FC, useState } from "react";
import { Button, DialogBase, Input } from "@/ui";
import { CreateAchievementViewModel } from "./create-achievement.vm";
import ReactDatePicker from "react-datepicker";
import DropdownMultiple from "@/ui/DropdownMultiple";
import AttachmentIcon from "@/assets/attatchment.svg";

export const CreateAchievementModal: FC<{ vm: MainPageViewModel; onCancel: () => void }> = observer(
  (x) => {
    const [vm] = useState(() => new CreateAchievementViewModel(x.onCancel));

    const v = vm.template;
    return (
      <DialogBase title="Новое достижение" isOpen onCancel={x.onCancel} width={550}>
        <form
          className="flex flex-col gap-5 w-full"
          onSubmit={(e) => {
            e.stopPropagation();
            vm.onSubmit();
          }}>
          <Input
            label="Название"
            placeholder="Новое достижение"
            value={v.title}
            onChange={(vv) => (v.title = vv)}
          />
          <div className="flex gap-5">
            <DropdownMultiple
              value={[v.type]}
              label="Тип мероприятия"
              onChange={(x) => (v.type = x.at(-1) ?? v.type)}
              render={(x) => x}
              options={["Обучение", "Творчество", "Общ. деятельность", "Спорт"]}
            />
            <div className="flex flex-col justify-between">
              <p className="text-text-primary/60 mb-2">День проведения</p>
              <ReactDatePicker
                aria-label="День проведения"
                id="deadline"
                selected={new Date(v.date)}
                onChange={(date) => (v.date = date ? date.toString() : new Date().toString())}
                placeholderText="1 января"
                className="rounded-lg px-3 h-[46px] border border-text-primary/20 w-28"
              />
            </div>
          </div>
          <div className="flex flex-col">
            <p className="text-text-primary/60 mb-2">Описание мероприятия</p>
            <textarea
              id="goal"
              value={v.description}
              onChange={(e) => (v.description = e.target.value)}
              className="px-3 py-2 h-28 text-text-primary text-base border border-text-primary/20 rounded-lg w-full"
              placeholder="Описание"
            />
          </div>
          <Input
            label="Ссылка на мероприятие"
            value={v.event_link}
            onChange={(vv) => (v.event_link = vv)}
            placeholder="https://example.com"
          />
          <Input
            label="Место проведения"
            value={v.place}
            onChange={(vv) => (v.place = vv)}
            placeholder="ВДНХ Павильон №75"
          />
          <div className="relative py-4 w-full px-4 rounded-2xl border border-dashed border-primary text-primary flex items-center justify-center">
            <AttachmentIcon />
            <p>Перетащите сюда или выберите подтверждающий файл</p>
            <input
              type="file"
              className="absolute inset-0 w-full h-full opacity-0"
              onChange={(e) => (vm.file = e.target.files?.item(0) ?? vm.file)}
            />
          </div>
          {vm.file?.name && <p className="text-text-primary">Выбран файл: {vm.file.name}</p>}
          <Button type="button" appearance="secondary" onClick={() => vm.onSubmit()}>
            Добавить задание
          </Button>
        </form>
      </DialogBase>
    );
  }
);
