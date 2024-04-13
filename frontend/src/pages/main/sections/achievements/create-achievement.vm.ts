import { AchievementEndpoint } from "api/endpoints/achievement.endpoint";
import { AchievementDto } from "api/models/achievement.model";
import { makeAutoObservable } from "mobx";
import { MainPageStore } from "../../main.vm";

export class CreateAchievementViewModel {
  constructor(private onCancel: () => void) {
    makeAutoObservable(this);
  }

  loading = false;

  template: AchievementDto.Template = {
    user_id: 0,
    title: "",
    date: new Date().toString(),
    place: "",
    description: "",
    type: "Творчество",
    event_link: "",
    file: new File([], "")
  };

  file: File | null = null;

  async onSubmit() {
    if (this.loading) return;

    if (
      !this.template.title ||
      !this.file ||
      !this.template.place ||
      !this.template.description ||
      !this.template.event_link
    ) {
      alert("Заполните все поля");
      return;
    }
    this.loading = true;

    this.template.file = this.file;

    try {
      const res = await AchievementEndpoint.create(this.template);

      MainPageStore.achievements.unshift(res);
      this.onCancel();
    } catch (e) {
      console.log(e);
    } finally {
      this.loading = false;
    }
  }
}
