import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../../main.vm";
import { FCVM } from "@/utils/fcvm";
import { IconButton, IconText, Separator } from "@/ui";
import { FC, useId } from "react";
import ChevronIcon from "@/assets/chevron2.svg";
import Lightning from "@/assets/lightning.svg";
import { HorizontalCarousel } from "@/components/swiper/HorizontalCarousel";
import { useIsMobile } from "@/hooks/useIsMobile";
import { Link } from "react-router-dom";
import { twMerge } from "tailwind-merge";
import { mockNews } from "../../../events/news.page";

export const NewsCard: FC<{ img: string; type: string; title: string; wide?: boolean }> = (x) => {
  return (
    <Link
      to={"/news"}
      className={twMerge(
        "flex flex-col overflow-hidden border bg-white border-text-primary/20 rounded-2xl w-[220px] h-[270px]",
        x.wide && "w-full"
      )}>
      <img
        src={x.img}
        alt="news"
        className="min-h-[120px] max-h-[120px] overflow-hidden w-full object-cover rounded-b-2xl"
      />
      <div className="px-5 py-4 flex-1 overflow-hidden">
        <span className="text-primary text-sm">{x.type}</span>
        <p className="multiline-ellipsis">{x.title}</p>
      </div>
    </Link>
  );
};

export const NewsSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  return (
    <section className="flex flex-col">
      <div className="flex justify-between items-center">
        <h2 className="font-medium text-xl px-2 py-2">Новости</h2>
        <div className="flex gap-2 h-8">
          <Link to="/news" className="flex items-center text-text-primary/60 gap-1">
            Все <ChevronIcon />
          </Link>
        </div>
      </div>
      <Separator className="my-2" />
      <HorizontalCarousel
        disablePadding
        mousewheel={{
          forceToAxis: true
        }}>
        {mockNews.map((news) => (
          <NewsCard key={news.id} img={news.img} type={news.type} title={news.title} />
        ))}
      </HorizontalCarousel>
    </section>
  );
});
