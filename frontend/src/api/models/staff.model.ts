export const MocMembers: StaffDto.User[] = [
  {
    id: "1",
    roles: ["Сетевые технологии"],
    fullName: "Иванова Анна Михайловна",
    phone: "+7 (921) 123-45-67",
    email: "ivanova.anna@mail.ru",
    telegram: "@ivanova_anna"
  },
  {
    id: "2",
    roles: ["Теория вероятности"],
    fullName: "Петров Сергей Васильевич",
    phone: "+7 (922) 234-56-78",
    email: "petrov.sergey@mail.ru",
    telegram: "@petrov_sergey"
  },
  {
    id: "3",
    roles: ["Дискретная математика"],
    fullName: "Смирнова Ольга Ивановна",
    phone: "+7 (923) 345-67-89",
    email: "smirnova.olga@mail.ru",
    telegram: "@smirnova_olga"
  },
  {
    id: "4",
    roles: ["Информационная безопасность"],
    fullName: "Кузнецова Мария Петровна",
    phone: "+7 (924) 456-78-90",
    email: "kuznetsova.maria@mail.ru",
    telegram: "@kuznetsova_maria"
  }
];

export const MocStaff: StaffDto.User[] = [
  {
    id: "5",
    roles: [],
    fullName: "Соколов Илья Дмитриевич",
    phone: "+7 (925) 567-89-01",
    email: "sokolov.ilya@mail.ru",
    telegram: "@sokolov_ilya"
  },
  {
    id: "6",
    roles: [],
    fullName: "Попова Ксения Романовна",
    phone: "+7 (926) 678-90-12",
    email: "popova.ksenia@mail.ru",
    telegram: "@popova_ksenia"
  }
];

export namespace StaffDto {
  export interface User {
    id: string;
    roles: string[];
    fullName: string;
    phone: string;
    email: string;
    telegram: string;
  }
}
