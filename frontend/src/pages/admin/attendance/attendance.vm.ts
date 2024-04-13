import { makeAutoObservable } from "mobx";

export class AttendanceViewModel {
  constructor() {
    makeAutoObservable(this);
  }

  onRequest(file: File[]) {
    console.log(file);
    this.loading = true;
  }

  loading = false;
}
