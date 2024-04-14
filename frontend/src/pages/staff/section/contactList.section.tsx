import Collapsible from "@/ui/Collapsible.tsx";
import { MocMembers, MocStaff } from "api/models/staff.model.ts";
import { StaffCard } from "../components/StaffCard.tsx";

export const ContactListSection = () => {
  return (
    <Collapsible title={"Мои преподаватели"}>
      <div
        className="grid gap-4 px-4 appear"
        style={{
          gridTemplateColumns: "repeat(auto-fit, minmax(256px, 1fr))"
        }}>
        {MocMembers.map((v) => (
          <StaffCard key={v.id} {...v} />
        ))}
      </div>
    </Collapsible>
  );
};

export const StaffListSection = () => {
  return (
    <Collapsible title={"Руководство вуза"}>
      <div
        className="grid gap-4 px-4 appear"
        style={{
          gridTemplateColumns: "repeat(auto-fit, minmax(256px, 1fr))"
        }}>
        {MocStaff.map((v) => (
          <StaffCard key={v.id} {...v} />
        ))}
      </div>
    </Collapsible>
  );
};
