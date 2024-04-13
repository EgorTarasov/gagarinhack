export namespace AchievementDto {
  export interface Template {
    user_id: number;
    title: string;
    date: string;
    place: string;
    description: string;
    type: string;
    event_link: string;
    file: File;
  }

  export interface Item {
    id: number;
    user_id: number;
    title: string;
    date: string;
    place: string;
    description: string;
    type: string;
    event_link: string;
  }
}
