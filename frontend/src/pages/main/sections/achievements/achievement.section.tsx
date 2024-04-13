import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../../main.vm";
import { FCVM } from "@/utils/fcvm";
import { IconButton, IconText, Separator } from "@/ui";
import { FC, useId } from "react";
import ChevronIcon from "@/assets/chevron2.svg";
import Lightning from "@/assets/lightning.svg";
import { HorizontalCarousel } from "@/components/swiper/HorizontalCarousel";
import MedalIcon from "./assets/medal.svg";
import { useIsMobile } from "@/hooks/useIsMobile";

export const AchievementCard: FC<{ name: string; type: string; iconClass?: string }> = (x) => {
  return (
    <li className="flex p-5 gap-3 rounded-2xl border border-text-primary/20 cursor-pointer">
      <MedalIcon className={x.iconClass} />
      <div className={`flex flex-col flex-1 ${x.iconClass}`}>
        <h3 className="font-medium text-lg leading-6 text-text-primary">{x.name}</h3>
        <IconText className={x.iconClass} icon={Lightning} alt="Тематика" text={x.type} />
      </div>
      <button className="my-auto">
        <ChevronIcon />
      </button>
    </li>
  );
};

export const AchievementSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  const leftControlId = useId();
  const rightControlId = useId();
  const isMobile = useIsMobile(1200);

  return (
    <section className="flex flex-col">
      <div className="flex justify-between items-center">
        <h2 className="font-medium text-xl px-2 py-2">Мои достижения</h2>
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
        <AchievementCard
          name="Хакатон «Гагарин хак»"
          type="Обучение"
          iconClass="text-event-education"
        />
        <AchievementCard iconClass="text-primary" name="Вокал" type="Обучение" />
        <AchievementCard
          name="Волонтёр на ДОД"
          type="Общ. деятельность"
          iconClass="text-event-sport"
        />
      </HorizontalCarousel>
    </section>
  );
});
