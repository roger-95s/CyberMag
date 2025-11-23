"use client";
import clsx from "clsx";

export function HoverBorderGradient({ children, className, containerClassName, as = "div", ...props }) {
  const Component = as;

  return (
    <Component
      className={clsx(
        "relative p-[2px] rounded-2xl group", // borde externo
        containerClassName
      )}
      {...props}
    >
      {/* Borde animado tipo neón */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>

      {/* Contenido de la card */}
      <div className={clsx("relative rounded-2xl bg-white dark:bg-gray-800", className)}>
        {children}
      </div>
    </Component>
  );
}
