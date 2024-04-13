import { EventDto, MockEvents } from "api/models/event.model.ts";
import { useEffect, useState } from "react";
import { Chip, Input } from "@/ui";
import SearchIcon from "@/assets/search.svg";
import { EventCard } from "@/components/cards/event-card.widget";
import api from "api/utils/api";
import { EventsEndpoint } from "api/endpoints/events.endpoint";
import { NewsDto } from "api/models/news.model";
import { NewsCard } from "../main/sections/news/news.section";

enum Filter {
  ForMe,
  Sport,
  Education,
  Volunteering,
  Creativity
}

export const mockNews: NewsDto.Item[] = [
  {
    id: "1",
    img: "/assets/news/learn.png",
    title: "Команда IThub взяла призовые места на чемпионате Москвы «Московские мастера»!",
    type: "Обучение"
  },
  {
    id: "2",
    img: "/assets/news/sport.png",
    title: "От волейбола до Dota 2: как устроена физкультура в IThub",
    type: "Спорт"
  },
  {
    id: "3",
    img: "/assets/news/concert.png",
    title:
      "Очень странные дела в IThub или вечеринка с мистическим вайбом: как прошел праздник в BASE",
    type: "Творчество"
  },
  {
    id: "4",
    img: "/assets/news/building.png",
    title:
      "Новое пространство для образования будущего: в 2024 году откроется корпус IThub на Дмитровской",
    type: "Спорт"
  }
] as const;

export const NewsPage = () => {
  const [search, setSearch] = useState("");
  const [filters, setFilters] = useState<Filter[]>([Filter.ForMe]);
  const [news, setNews] = useState<NewsDto.Item[]>(mockNews);

  const handleFilter = (filter: Filter) => {
    if (filters.includes(filter)) {
      setFilters(filters.filter((f) => f !== filter));
    } else {
      setFilters([...filters, filter]);
    }
  };

  return (
    <div className="flex flex-col gap-4 px-4 mx-auto max-w-screen-desktop fade-enter-done mt-6 sm:mt-10">
      <Input
        id={"search"}
        placeholder={"Поиск"}
        rightIcon={<SearchIcon />}
        className=""
        value={search}
        onChange={setSearch}
      />
      <div className={"flex items-center gap-2 flex-wrap"}>
        <Chip
          title={"Для меня"}
          onClick={() => handleFilter(Filter.ForMe)}
          isActive={filters.includes(Filter.ForMe)}
        />
        <Chip
          title={"Спорт"}
          onClick={() => handleFilter(Filter.Sport)}
          isActive={filters.includes(Filter.Sport)}
        />
        <Chip
          title={"Обучение"}
          onClick={() => handleFilter(Filter.Education)}
          isActive={filters.includes(Filter.Education)}
        />
        <Chip
          title={"Волонтёрство"}
          onClick={() => handleFilter(Filter.Volunteering)}
          isActive={filters.includes(Filter.Volunteering)}
        />
        <Chip
          title={"Творчество"}
          onClick={() => handleFilter(Filter.Creativity)}
          isActive={filters.includes(Filter.Creativity)}
        />
      </div>
      <ul
        className="grid gap-4"
        style={{
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))"
        }}>
        {news.map((v, i) => (
          <NewsCard title={v.title} img={v.img} type={v.type} key={i} wide />
        ))}
      </ul>
    </div>
  );
};
