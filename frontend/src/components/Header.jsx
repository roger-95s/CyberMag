import { useEffect, useState } from "react";
import { Shield, Sun, Moon, Menu, X } from "lucide-react";
import NotFoundImage from "../assets/img/Page_not_Found_404.png";

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
  const [selectedSection, setSelectedSection] = useState(null);

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

  const toggleDarkMode = () => setIsDarkMode((prev) => !prev);
  const toggleMenu = () => setMenuOpen((prev) => !prev);
  const handleSectionClick = (section) => setSelectedSection(section);

  return (
    <>
      <header className="sticky top-0 z-50 bg-white dark:bg-[#0a0f1a] border-b border-gray-300 dark:border-gray-800 shadow-md transition-colors duration-300">
        <div className="container mx-auto flex items-center justify-between px-4 py-3">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <Shield className="text-cyan-500 w-6 h-6 dark:text-cyan-400" />
            <span className="text-gray-900 dark:text-white font-bold text-xl tracking-wide">
              CyberMag
            </span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex gap-6 text-sm font-medium">
            {["NEWS", "REPORTS", "ANALYSIS", "ABOUT"].map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => handleSectionClick(item)}
                className="text-gray-700 dark:text-gray-300 hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 cursor-pointer"
              >
                {item}
              </button>
            ))}
          </nav>

          {/* Right Section */}
          <div className="flex items-center gap-2 md:gap-4">
            {/* Dark Mode Toggle */}
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-full bg-gray-200 dark:bg-gray-800 hover:bg-cyan-500 transition-colors duration-300 text-cyan-600 dark:text-cyan-400 hover:text-white"
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
              className="md:hidden p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-cyan-600 dark:text-cyan-400 transition-all"
              onClick={toggleMenu}
              aria-label="Toggle Navigation Menu"
            >
              {menuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Dropdown */}
        <div
          className={`md:hidden px-4 pb-4 transition-all duration-300 ease-in-out ${
            menuOpen
              ? "max-h-60 opacity-100"
              : "max-h-0 opacity-0 overflow-hidden"
          }`}
        >
          <nav className="flex flex-col gap-3 text-sm font-medium text-gray-700 dark:text-gray-300">
            {["NEWS", "REPORTS", "ANALYSIS", "ABOUT"].map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => handleSectionClick(item)}
                className="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors bg-transparent border-none p-0 m-0 text-left cursor-pointer"
              >
                {item}
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Imagen Not Found */}
      {selectedSection && (
        <div className="flex flex-col items-center justify-center py-10 bg-gray-50 dark:bg-[#0a0f1a] border-t border-gray-200 dark:border-gray-800 transition-colors duration-300">
          <img
            src={NotFoundImage}
            alt="Page Not Found"
            className="w-80 md:w-96 opacity-90 mb-4"
          />
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            Section{" "}
            <span className="text-cyan-600 dark:text-cyan-400 font-semibold">
              {selectedSection}
            </span>{" "}
            not available yet.
          </p>
        </div>
      )}
    </>
  );
};

export default Header;
