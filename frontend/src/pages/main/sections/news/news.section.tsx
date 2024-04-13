import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../../main.vm";
import { FCVM } from "@/utils/fcvm";
import { Separator } from "@/ui";
import { FC } from "react";
import ChevronIcon from "@/assets/chevron2.svg";
import { HorizontalCarousel } from "@/components/swiper/HorizontalCarousel";
import { Link } from "react-router-dom";
import { twMerge } from "tailwind-merge";

export const NewsCard: FC<{
  id: string;
  img: string;
  type: string;
  title: string;
  wide?: boolean;
}> = (x) => {
  return (
    <a
      href={`https://ithub.ru/news/${x.id}`}
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
    </a>
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
        {vm.news.map((news) => (
          <NewsCard key={news.id} img={news.img} type={news.type} title={news.title} id={news.id} />
        ))}
      </HorizontalCarousel>
    </section>
  );
});
