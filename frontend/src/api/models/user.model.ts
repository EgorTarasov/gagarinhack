import { EventDto } from "./event.model";

// {
//     "id": 3,
//     "email": "string@string.ru",
//     "first_name": "string",
//     "last_name": "string",
//     "created_at": "2024-04-13T16:04:36.025870",
//     "updated_at": "2024-04-13T16:04:36.025870"
// }
export namespace UserDto {
  export interface Item {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    created_at: string;
    updated_at: string;
  }
}
