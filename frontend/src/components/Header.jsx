import React, { useEffect, useState } from "react";
import { Shield, Sun, Moon } from "lucide-react";

const Header = () => {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Inicializa desde localStorage o media query
    if (typeof window !== "undefined") {
      return (
        localStorage.getItem("theme") === "dark" ||
        (!localStorage.getItem("theme") &&
          window.matchMedia("(prefers-color-scheme: dark)").matches)
      );
    }
    return false;
  });

  // Aplica/remueve clase "dark" y guarda en localStorage
  useEffect(() => {
    const root = document.documentElement;
    if (isDarkMode) {
      root.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      root.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    setIsDarkMode((prev) => !prev);
  };

  return (
    <header className="sticky top-0 z-50 bg-[#0a0f1a] border-b border-gray-800 shadow-m">
      <div className="container mx-auto flex items-center justify-between px-4 py-3">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <Shield className="text-cyan-400 w-6 h-6" />
          <span className="text-white font-bold text-xl tracking-wide">
            CyberMag
          </span>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex gap-6 text-sm font-medium">
          <a
            href="#"
            className="text-gray-300 hover:text-cyan-400 transition-colors"
          >
            NEWS
          </a>
          <a
            href="#"
            className="text-gray-300 hover:text-cyan-400 transition-colors"
          >
            REPORTS
          </a>
          <a
            href="#"
            className="text-gray-300 hover:text-cyan-400 transition-colors"
          >
            ANALYSIS
          </a>
          <a
            href="#"
            className="text-gray-300 hover:text-cyan-400 transition-colors"
          >
            ABOUT
          </a>
        </nav>

        {/* Dark Mode Toggle */}
        <button
          onClick={toggleDarkMode}
          className="ml-4 p-2 rounded-full bg-gray-800 hover:bg-cyan-600 transition-colors duration-300 text-cyan-400 hover:text-white"
          aria-label="Toggle Dark Mode"
        >
          {isDarkMode ? (
            <Sun className="w-5 h-5" />
          ) : (
            <Moon className="w-5 h-5" />
          )}
        </button>
      </div>
    </header>
  );
};

export default Header;
