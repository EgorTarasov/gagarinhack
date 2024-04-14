import { observer } from "mobx-react-lite";
import { CSSProperties } from "react";
import { twMerge } from "tailwind-merge";
import LogoSvg from "@/assets/logo.svg";

export const Logo = observer(
  ({ width, className }: { width?: CSSProperties["width"]; className?: string }) => (
    <div
      aria-label={"Логотип компании: IT Hub"}
      className={twMerge("h-auto", className)}
      style={{
        width: width ?? 150
      }}>
      <LogoSvg />
    </div>
  )
);
