import { Button, Checkbox, IconText } from "@/ui";
import { Link } from "react-router-dom";
import { twMerge } from "tailwind-merge";
import Chevron from "@/assets/chevron2.svg";
import CalendarIcon from "@/assets/calendar.svg";
import LightningIcon from "@/assets/lightning.svg";
import PointIcon from "@/assets/marker.svg";

interface Props {
  onBuildRoute?: () => void;
  isCompleted: boolean;
  schedule: string;
  title: string;
  location: string;
  lessonType: string;
}

export const TaskCard = ({ onBuildRoute, ...item }: Props) => {
  return (
    <a
      href="https://yandex.ru/maps/?rtext=~55.835902,37.631128"
      className={twMerge(
        "relative flex gap-3 items-start py-2 transition-all hover:bg-black/5 rounded-lg px-2",
        item.isCompleted && "opacity-60"
      )}>
      <Checkbox
        className={"mt-1 text-primary pointer-events-none"}
        disabled
        checked={item.isCompleted}
        ariaHidden
      />
      <div className="flex flex-col">
        <p className="text-lg leading-none">{item.title}</p>
        <ul className="flex flex-wrap gap-2 mt-3">
          <IconText icon={CalendarIcon} text={item.schedule} alt="Конец срока" />
          <IconText iconPrimary icon={LightningIcon} text={item.lessonType} alt="Тип занятия" />
          <IconText icon={PointIcon} text={item.location} alt="Локация" />
        </ul>
      </div>
      {onBuildRoute ? (
        <Button
          disabled={item.isCompleted}
          className="ml-auto my-auto w-fit px-3"
          appearance="secondary"
          onClick={() => onBuildRoute?.()}>
          {item.isCompleted ? "Завершено" : "В процессе"}
        </Button>
      ) : (
        <Chevron className="ml-auto my-auto" />
      )}
    </a>
  );
};
