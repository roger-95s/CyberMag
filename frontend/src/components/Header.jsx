import React, { useState, useEffect } from "react";
import { Shield, Sun, Moon, Menu, X } from "lucide-react";

const Header = () => {
  const [isDark, setIsDark] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Dark mode toggle
  useEffect(() => {
    const html = document.documentElement;
    isDark ? html.classList.add("dark") : html.classList.remove("dark");
  }, [isDark]);

  return (
    <header className="sticky top-0 z-50 bg-[#0a0f1a] border-b border-gray-800 shadow-md">
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
          {["NEWS", "REPORTS", "ANALYSIS", "ABOUT"].map((item) => (
            <a
              key={item}
              href="#"
              className="text-gray-300 hover:text-cyan-400 transition-colors"
            >
              {item}
            </a>
          ))}
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-4">
          {/* Dark mode toggle */}
          <button
            onClick={() => setIsDark(!isDark)}
            className="text-cyan-400 hover:text-white transition-colors"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
          </button>

          {/* Burger menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-cyan-400 hover:text-white transition"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <div
  className={`md:hidden bg-[#0a0f1a] border-t border-gray-800 px-4 py-2 space-y-2 transform transition-all duration-300 ${
    isMenuOpen ? "max-h-60 opacity-100" : "max-h-0 opacity-0 overflow-hidden"
  }`}
>
  {["NEWS", "REPORTS", "ANALYSIS", "ABOUT"].map((item) => (
    <a
      key={item}
      href="#"
      className="block text-gray-300 hover:text-cyan-400 transition-colors"
      onClick={() => setIsMenuOpen(false)} // Cierra al hacer clic
    >
      {item}
    </a>
  ))}
</div>

      
    </header>
  );
};

export default Header;
