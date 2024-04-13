import { makeAutoObservable } from "mobx";
import io from "socket.io-client";

interface MessageItem {
  message: string;
  isUser: boolean;
  link?: string;
}

export class AssistantViewModel {
  constructor(public message: string) {
    makeAutoObservable(this);
    if (message) {
      this.sendMessage();
    }

    this.socket.on("message", (v) => this.receiveMessage(v));
  }

  socket = io(import.meta.env.VITE_SOCKET_URL, {
    transports: ["websocket"],
    upgrade: false
  });

  messages: MessageItem[] = [];
  sendMessage = () => {
    this.messages.push({ message: this.message, isUser: true });
    this.socket.emit("message", this.message);
    this.message = "";
  };

  receiveMessage = (message: string) => {
    this.messages.push({ message, isUser: false });
  };
}
