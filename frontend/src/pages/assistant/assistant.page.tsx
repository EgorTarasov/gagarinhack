import { useState } from "react";
import { useLocation } from "react-router-dom";
import { AssistantViewModel } from "./assistant.vm";
import { observer } from "mobx-react-lite";
import { Input } from "@/ui";
import SendIcon from "@/assets/send.svg";

export const AssistantPage = observer(() => {
  const location = useLocation();
  const message = location.state?.message;
  const [vm] = useState(() => new AssistantViewModel(message ?? ""));

  return (
    <div className="flex h-full w-full py-6 flex-col gap-4 sm:px-4 mx-auto max-w-screen-desktop">
      <div className="flex-1 flex flex-col-reverse overflow-y-auto">
        <ul className="flex flex-col gap-3">
          {vm.messages.map((item, index) => (
            <li
              key={index}
              className={`${item.isUser ? "justify-end" : "justify-start"} flex gap-2`}>
              <div
                className={`${
                  item.isUser
                    ? "bg-primary text-white rounded-tl-xl rounded-br-xl"
                    : "bg-text-primary/5 text-text-primary rounded-tr-xl rounded-bl-xl"
                } p-2`}>
                {item.message}
              </div>
            </li>
          ))}
        </ul>
      </div>
      <form
        className="w-full"
        onSubmit={(e) => {
          e.preventDefault();
          vm.sendMessage();
        }}>
        <Input
          className="w-full max-w-none"
          rightIcon={<SendIcon />}
          placeholder="Введите вопрос"
          aria-label="Введите ваш вопрос здесь"
          value={vm.message}
          onChange={(v) => (vm.message = v)}
        />
      </form>
    </div>
  );
});
