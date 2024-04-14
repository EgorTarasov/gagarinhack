import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../../main.vm";
import { FCVM } from "@/utils/fcvm";
import { IconButton, IconText, Separator } from "@/ui";
import { FC, ReactElement, useId } from "react";
import ChevronIcon from "@/assets/chevron2.svg";
import Calendar from "@/assets/calendar.svg";
import { HorizontalCarousel } from "@/components/swiper/HorizontalCarousel";
import FootballIcon from "./assets/football.svg";
import LearnIcon from "./assets/learn.svg";
import VocalIcon from "./assets/vocal.svg";
import { useIsMobile } from "@/hooks/useIsMobile";

const Card: FC<{ name: string; icon: ReactElement; time: string }> = (x) => {
  return (
    <li className="flex p-5 gap-3 rounded-2xl border border-text-primary/20 cursor-pointer">
      {x.icon}
      <div className="flex flex-col flex-1">
        <h3 className="font-medium text-lg leading-6">{x.name}</h3>
        <IconText icon={Calendar} alt="Время" text={x.time} />
      </div>
      <button className="my-auto">
        <ChevronIcon />
      </button>
    </li>
  );
};

export const CommunitiesSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  const leftControlId = useId();
  const rightControlId = useId();
  const isMobile = useIsMobile(1200);

  return (
    <section className="flex flex-col">
      <div className="flex justify-between items-center">
        <h2 className="font-medium text-xl px-2 py-2">Рекомендованные сообщества</h2>
        <div className="flex gap-2 h-8">
          <IconButton id={leftControlId} icon={() => <ChevronIcon className="rotate-180" />} />
          <IconButton id={rightControlId} icon={ChevronIcon} />
        </div>
      </div>
      <Separator className="my-2" />
      <HorizontalCarousel
        slidesPerView={isMobile ? 1 : 3}
        disablePadding
        navigation={{
          prevEl: `#${CSS.escape(leftControlId)}`,
          nextEl: `#${CSS.escape(rightControlId)}`,
          enabled: true
        }}>
        <Card icon={<FootballIcon />} name="Футбол" time="ПН 12:30" />
        <Card icon={<VocalIcon />} name="Вокал" time="ВТ 14:30" />
        <Card icon={<LearnIcon />} name="Дизайн-клуб" time="ВТ 15:30" />
      </HorizontalCarousel>
    </section>
  );
});
