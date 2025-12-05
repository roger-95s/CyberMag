// import { useEffect, useState } from "react";
import { Shield } from "lucide-react";
import { NavLinks } from "./NavbarLinks";
import DarkModeToggle from "./Darkmode";

const Header = () => {
  return (
    <>
      <header className="sticky top-0 z-50 bg-white dark:bg-[#0a0f1a] border-b border-gray-300 dark:border-gray-800 shadow-md transition-colors duration-300">
        <div className="container mx-auto flex items-center px-4 py-3">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <Shield className="text-cyan-500 w-10 h-10 dark:text-cyan-400" />
            <span className="text-gray-900 dark:text-white font-bold text-xl tracking-wide">
              <a
                href="/CyberMag"
                className="hover:text-cyan-500 transition-colors"
              >
                CyberMag
              </a>
            </span>
          </div>

          {/* NavLinks */}
          <div className="flex items-center gap-6 ml-auto">
            <NavLinks />
          </div>

          {/* DarkModeToggle */}
          <div className="ml-8">
            <DarkModeToggle />
          </div>
        </div>
      </header>
    </>
  );
};
export default Header;
