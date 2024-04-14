import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../../main.vm";
import { FCVM } from "@/utils/fcvm";
import { IconButton, Separator } from "@/ui";
import { useId } from "react";
import ChevronIcon from "@/assets/chevron2.svg";
import { TaskCard } from "@/components/cards/task.card";

export const ScheduleSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  const leftControlId = useId();
  const rightControlId = useId();

  const currentDate = new Intl.DateTimeFormat("ru", { day: "numeric", month: "long" }).format(
    Date.now()
  );

  return (
    <section className="flex flex-col">
      <div className="flex justify-between items-center">
        <h2 className="font-medium text-xl px-2 py-2">Моё расписание</h2>
        <div className="flex gap-2 h-8">
          <IconButton id={leftControlId} icon={() => <ChevronIcon className="rotate-180" />} />
          <div className="flex items-center h-full justify-center px-3 bg-text-primary/5 rounded-lg">
            {currentDate}
          </div>
          <IconButton id={rightControlId} icon={ChevronIcon} />
        </div>
      </div>
      <Separator className="my-2" />
      <ul className="">
        {/* {
          vm.schedule.map((item, index) => (
            <TaskCard key={index} {...item} />
          ))
        } */}
        <TaskCard
          isCompleted={true}
          schedule="10:00-12:00"
          title="Математика"
          location="Корпус 1"
          lessonType="Лекция"
        />
        <TaskCard
          isCompleted={false}
          schedule="12:15-13:45"
          title="Английский язык"
          location="Корпус 2"
          lessonType="Практика"
        />
        <TaskCard
          isCompleted={false}
          schedule="14:00-15:30"
          title="Алгоритмы дискретной математики"
          location="Корпус 1"
          lessonType="Лекция"
        />
      </ul>
    </section>
  );
});
