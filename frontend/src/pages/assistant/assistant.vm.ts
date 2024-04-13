import { makeAutoObservable } from "mobx";

interface MessageItem {
  message: string;
  isUser: boolean;
  link?: string;
}

interface MessageEvent {
  id: string;
  text?: string;
  metadata?: string[];
}

type Message = string;

export class AssistantViewModel {
  constructor(public message: string) {
    makeAutoObservable(this);
    if (message) {
      this.sendMessage();
    }

    this.ws = new WebSocket("ws://localhost:8080");
    this.ws.addEventListener("ключ", (data) => console.log(data));
  }

  ws;

  messages: MessageItem[] = [];
  sendMessage = () => {
    if (!this.message.trim().length) return;

    this.messages.push({ message: this.message, isUser: false });
    this.message = "";
  };

  receiveMessage = (message: string) => {
    this.messages.push({ message, isUser: false });
  };
}
