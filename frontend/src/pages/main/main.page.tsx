import { useState } from "react";
import { AssistantSection } from "./sections/assistant.section";
import { MainPageViewModel } from "./main.vm";
import { observer } from "mobx-react-lite";
import { ScheduleSection } from "./sections/schedule/schedule.section";
import { CommunitiesSection } from "./sections/communities/communities.section";
import { AchievementSection } from "./sections/achievements/achievement.section";
import { NewsSection } from "./sections/news/news.section";

const card = "bg-white w-full rounded-2xl sm:p-4";

export const MainPage = observer(() => {
  const [vm] = useState(() => new MainPageViewModel());

  return (
    <div className="flex flex-col gap-4 sm:px-4 mx-auto max-w-screen-desktop">
      <AssistantSection vm={vm} />
      {!vm.isLoading && (
        <div className="flex flex-col gap-4 w-full mx-auto max-w-screen-desktop appear">
          <div className={card}>
            <ScheduleSection vm={vm} />
          </div>
          <div className={card}>
            <NewsSection vm={vm} />
          </div>
          <div className={card}>
            <CommunitiesSection vm={vm} />
          </div>
          <div className={card}>
            <AchievementSection vm={vm} />
          </div>
        </div>
      )}
    </div>
  );
});
