import { useState } from "react";
import { useLocation } from "react-router-dom";
import { AssistantViewModel } from "./assistant.vm";
import { observer } from "mobx-react-lite";
import { Input } from "@/ui";
import SendIcon from "@/assets/send.svg";
import AssistantIcon from "./assistant.svg";

export const AssistantPage = observer(() => {
  const location = useLocation();
  const message = location.state?.message;
  const [vm] = useState(() => new AssistantViewModel(message ?? ""));

  return (
    <div className="relative flex h-full w-full py-6 px-4 flex-col gap-4 mx-auto max-w-screen-desktop overflow-hidden">
      <div className="flex-1 flex flex-col-reverse overflow-y-auto h-full">
        <ul className="flex flex-col gap-3">
          {vm.messages.map((item, index) => (
            <li
              key={index}
              className={`${item.isUser ? "justify-end" : "justify-start"} flex gap-2`}>
              <div
                className={`p-5 rounded-2xl text-text-primary max-w-[70%]
                ${
                  item.isUser
                    ? "bg-primary/20 rounded-br-none"
                    : "bg-text-primary/5 rounded-bl-none border border-text-primary/5"
                }`}>
                {item.message}
              </div>
            </li>
          ))}
          {!vm.messages.length && (
            <div className="flex items-center bg-white rounded-2xl p-4 border border-text-primary/20">
              <AssistantIcon />
              <div className="flex flex-col gap-2">
                <h2 className="font-semibold text-2xl">Привет! Чем могу помочь?</h2>
                <p className="text-text-primary/80">
                  Напишите свой вопрос на тему обучения и я постараюсь помочь вам.
                </p>
              </div>
            </div>
          )}
        </ul>
      </div>
      <form
        className="w-full min-h-fit"
        onSubmit={(e) => {
          e.preventDefault();
          vm.sendMessage();
        }}>
        <Input
          className="w-full max-w-none"
          rightIcon={<SendIcon />}
          placeholder="Введите вопрос"
          disabled={vm.loading}
          aria-label="Введите ваш вопрос здесь"
          value={vm.message}
          onChange={(v) => (vm.message = v)}
        />
      </form>
    </div>
  );
});
