import { Tabs } from "@/ui/Tabs.tsx";
import SearchIcon from "@/assets/search.svg";
import { Button, DialogBase, Input } from "@/ui";
import { useEffect, useState } from "react";
import { ContactListSection, StaffListSection } from "./section/contactList.section.tsx";
import { MeetingSection } from "./section/meeting.section.tsx";
import { observer } from "mobx-react-lite";
import { twMerge } from "tailwind-merge";

export const ContactsPage = observer(() => {
  const [search, setSearch] = useState("");
  const [answer, setAnswer] = useState<string>("");

  return (
    <>
      <div className="py-6 mt-4 flex flex-col gap-4 mx-auto max-w-screen-desktop">
        <Input
          id={"search"}
          placeholder={"Поиск"}
          rightIcon={<SearchIcon />}
          className="px-4"
          value={search}
          onChange={setSearch}
        />
        <StaffListSection />
        <ContactListSection />
      </div>
    </>
  );
});
