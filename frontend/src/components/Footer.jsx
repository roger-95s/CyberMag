import { Mail, Shield } from "lucide-react";
import { Link } from "react-router-dom";

function NavLinks() {
  return (
    <nav className="flex gap-6 text-sm font-medium">


      <Link
        to="/about"
        className="rounded-md px-3 py-2 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-white/10 transition"
      >
        About us
      </Link>
   
      <Link
        to="/pricing"
        className="rounded-md px-3 py-2 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-white/10 transition"
      >
        Pricing & Plans
      </Link>
      <Link
        to="/contact"
        className="rounded-md px-3 py-2 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-white/10 transition"
      >
        Contact
      </Link>
    </nav>
  );
}

export default function Footer() {
  return (
    <footer className="w-full bg-white dark:bg-[#0a0f1a] text-black dark:text-white py-12">
      <div className="container mx-auto">
        <div className="w-full bg-white dark:bg-[#0a0f1a] border-gray-300 dark:border-gray-800 px-10 py-12 flex flex-col md:flex-row justify-between items-center gap-10">
          {/* IZQUIERDA: LOGO + Nombre + Texto */}
          <div className="text-center md:text-left">
            <div className="flex justify-center md:justify-start items-center gap-3">
              <Shield className="text-cyan-500 w-10 h-10 dark:text-cyan-400" />
              <h2 className="text-xl font-semibold">CyberMag</h2>
            </div>

            <p className="text-gray-700 dark:text-gray-400 text-sm mt-3 w-64 mx-auto md:mx-0">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </p>
          </div>

          {/* DERECHA: EMAIL + NAV LINKS */}
          <div className="flex flex-col items-center md:items-end gap-6">
            {/* Email pill */}
            <div className="flex items-center gap-3 border border-gray-300 dark:border-gray-700 px-5 py-3 rounded-xl bg-black/10 dark:bg-black/40 backdrop-blur-sm cursor-pointer hover:border-gray-500 transition">
              <Mail size={18} className="text-gray-700 dark:text-gray-300" />
              <span className="text-gray-700 dark:text-gray-300 text-sm">
                info@cybermag.com
              </span>
            </div>

            {/* Nav Links */}
            <NavLinks />
          </div>
        </div>
      </div>

      {/* COPYRIGHT */}
      <p className="text-center text-gray-500 dark:text-gray-600 text-xs mt-6">
        © {new Date().getFullYear()} CyberMag — All rights reserved.
      </p>
    </footer>
  );
}
