import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../../main.vm";
import { FCVM } from "@/utils/fcvm";
import { Button, DialogBase, IconButton, IconText, Separator } from "@/ui";
import { FC, useId, useState } from "react";
import ChevronIcon from "@/assets/chevron2.svg";
import Lightning from "@/assets/lightning.svg";
import { HorizontalCarousel } from "@/components/swiper/HorizontalCarousel";
import MedalIcon from "./assets/medal.svg";
import PlusIcon from "@/assets/plus.svg";
import { useIsMobile } from "@/hooks/useIsMobile";
import { CreateAchievementModal } from "./create-achievement.modal";

export const AchievementCard: FC<{
  name: string;
  type: string;
  iconClass?: string;
  onClick?: () => void;
}> = (x) => {
  return (
    <li>
      <button
        className="flex p-5 gap-3 rounded-2xl border border-text-primary/20 cursor-pointer"
        onClick={() => x.onClick?.()}>
        <MedalIcon className={x.iconClass} />
        <div className={`flex flex-col flex-1 ${x.iconClass}`}>
          <h3 className="font-medium text-lg leading-6 text-text-primary">{x.name}</h3>
          <IconText className={x.iconClass} icon={Lightning} alt="Тематика" text={x.type} />
        </div>
        <button className="my-auto">
          <ChevronIcon />
        </button>
      </button>
    </li>
  );
};

function formatDate(date: Date) {
  const months = [
    "Января",
    "Февраля",
    "Марта",
    "Апреля",
    "Мая",
    "Июня",
    "Июля",
    "Августа",
    "Сентября",
    "Октября",
    "Ноября",
    "Декабря"
  ];

  // Extract the day, month, and year from the date
  const day = date.getDate();
  const month = date.getMonth();
  const year = date.getFullYear();

  // Format the day to ensure it is always two digits
  const formattedDay = day < 10 ? `0${day}` : day;

  // Combine the parts to format the date as "DD Month YYYY"
  return `${formattedDay} ${months[month]} ${year}`;
}

const TitleText: FC<{ title: string; text: string; asLink?: boolean }> = ({
  title,
  text,
  asLink
}) => (
  <div className="flex gap-2 flex-col">
    <h3 className="text-text-primary/60">{title}</h3>
    {!asLink ? (
      <p>{text}</p>
    ) : (
      <a href={text} target="_blank" rel="noreferrer" className="w-fit">
        {text}
      </a>
    )}
  </div>
);

export const AchievementSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  const [showCreateAchievement, setShowCreateAchievement] = useState(false);
  const leftControlId = useId();
  const rightControlId = useId();
  const isMobile = useIsMobile(1200);

  return (
    <>
      {showCreateAchievement && (
        <CreateAchievementModal vm={vm} onCancel={() => setShowCreateAchievement(false)} />
      )}
      <DialogBase
        width={550}
        title={vm.selectedAchievement?.title ?? "Хакатон"}
        onCancel={() => (vm.selectedAchievement = null)}
        isOpen={vm.selectedAchievement !== null}>
        <div className="flex flex-col gap-3">
          <TitleText title="Дата участия" text={vm.selectedAchievement?.date ?? ""} />
          <TitleText
            title="Описание мероприятия"
            text={vm.selectedAchievement?.description ?? ""}
          />
          <TitleText
            title="Ссылка на мероприятие"
            text={vm.selectedAchievement?.description ?? "test"}
            asLink
          />
          <button onClick={() => vm.downloadCertificate()} className="text-primary underline w-fit">
            Сертификат победителя
          </button>
          <div className="flex gap-2 w-full">
            <Button className="flex-1">Редактировать</Button>
            <Button className="flex-1" appearance="secondary">
              Удалить
            </Button>
          </div>
        </div>
      </DialogBase>
      <section className="flex flex-col">
        <div className="flex items-center">
          <h2 className="font-medium text-xl px-2 py-2">Мои достижения</h2>
          <IconButton icon={PlusIcon} onClick={() => setShowCreateAchievement(true)} />
          <div className="flex-1"></div>
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
          {vm.achievements.map((x) => (
            <AchievementCard
              key={x.id}
              onClick={() => (vm.selectedAchievement = x)}
              name={x.title}
              type={x.type}
              iconClass="text-event-education"
            />
          ))}
        </HorizontalCarousel>
        {vm.achievements.length === 0 && (
          <div className="flex flex-col items-center justify-center py-4 gap-2">
            <MedalIcon className="text-gray-400" />
            <p className="text-text-primary/60">У вас пока нет достижений</p>
          </div>
        )}
      </section>
    </>
  );
});
