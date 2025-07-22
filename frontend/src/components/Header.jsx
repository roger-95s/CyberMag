import { useEffect, useState } from "react";
import { Shield, Sun, Moon, Menu, X } from "lucide-react";

const Header = () => {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    if (typeof window !== "undefined") {
      return (
        localStorage.getItem("theme") === "dark" ||
        (!localStorage.getItem("theme") &&
          window.matchMedia("(prefers-color-scheme: dark)").matches)
      );
    }
    return false;
  });

  const [menuOpen, setMenuOpen] = useState(false);

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

  const toggleMenu = () => {
    setMenuOpen((prev) => !prev);
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

        {/* Desktop Navigation */}
        <nav className="hidden md:flex gap-6 text-sm font-medium">
          <button type="button" className="text-gray-300 hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 cursor-pointer">
            NEWS
          </button>
          <button type="button" className="text-gray-300 hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 cursor-pointer">
            REPORTS
          </button>
          <button type="button" className="text-gray-300 hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 cursor-pointer">
            ANALYSIS
          </button>
          <button type="button" className="text-gray-300 hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 cursor-pointer">
            ABOUT
          </button>
        </nav>

        <div className="flex items-center gap-2 md:gap-4">
          {/* Dark Mode Toggle */}
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-full bg-gray-800 hover:bg-cyan-600 transition-colors duration-300 text-cyan-400 hover:text-white"
            aria-label="Toggle Dark Mode"
          >
            {isDarkMode ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </button>

          {/* Mobile Menu Toggle */}
          <button
            className="md:hidden p-2 rounded hover:bg-gray-700 text-cyan-400 transition-all"
            onClick={toggleMenu}
            aria-label="Toggle Navigation Menu"
          >
            {menuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation Dropdown */}
      <div
        className={`md:hidden px-4 pb-4 transition-all duration-300 ease-in-out ${menuOpen ? "max-h-60 opacity-100" : "max-h-0 opacity-0 overflow-hidden"
          }`}
      >
        <nav className="flex flex-col gap-3 text-sm font-medium text-gray-300">
          <button type="button" className="hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 text-left cursor-pointer">
            NEWS
          </button>
          <button type="button" className="hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 text-left cursor-pointer">
            REPORTS
          </button>
          <button type="button" className="hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 text-left cursor-pointer">
            ANALYSIS
          </button>
          <button type="button" className="hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 text-left cursor-pointer">
            ABOUT
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
