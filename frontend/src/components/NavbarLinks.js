import { Link } from "react-router-dom";

function NavLinks() {
  return (
    <div className="hidden md:flex gap-6 text-sm font-medium text-gray-700 dark:text-gray-300">
      <div className="flex space-x-4">
        <Link
          to="/"
          className="rounded-md bg-gray-950/50 px-3 py-2 text-sm font-medium text-white"
        >
          Home
        </Link>
        <Link
          to="/posts"
          className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-white/5 hover:text-white"
        >
          Posts
        </Link>
        <Link
          to="/about"
          className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-white/5 hover:text-white"
        >
          About us
        </Link>
      </div>
    </div>
  );
}

export { NavLinks };
