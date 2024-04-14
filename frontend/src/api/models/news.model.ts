export namespace NewsDto {
  export interface Item {
    id: string;
    img: string;
    type: string;
    title: string;
  }

  export interface Result {
    title: string;
    description: string;
    image_link: string;
    id: number;
  }

  export const convertDto = (item: Result): Item => {
    return {
      id: item.id.toString(),
      img: item.image_link,
      type: "news",
      title: item.title
    };
  };
}
