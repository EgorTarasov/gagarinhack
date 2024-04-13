import { EventDto } from "./event.model";

export namespace UserDto {
  export interface Item {
    first_name: string;
    last_name: string;
    middle_name?: string;
    email: string;
    number: string;
    adaptation_target: string;
    starts_work_at: string;
    position_id: number;
    id: number;
    position: {
      name: string;
      id: number;
    };
  }

  export interface Update {
    first_name: string;
    last_name: string;
    middle_name?: string;
    email: string;
    number: string;
    adaptation_target: string;
    starts_work_at: string;
    position_id: number;
    role_id?: number;
  }

  export interface Current {
    first_name: string;
    last_name: string;
    middle_name?: string;
    email: string;
    number: string;
    adaptation_target: string;
    starts_work_at: string;
    position_id: number;
    role_id?: number;
    id: number;
    position: {
      name: string;
      id: number;
    };
    events: EventDto.Item[];
    mentors: Item[];
    interests?: {
      id: number;
      name: string;
    }[];
    fact?: {
      question: string;
      answer: string;
      id: number;
    };
    telegram?: {
      id: number;
      first_name: string;
      last_name: string;
      username?: string;
      photo_url: string;
      auth_date: number;
      hash: string;
    };
  }
}
