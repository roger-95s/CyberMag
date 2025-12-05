import { Link } from "react-router-dom";

function NavLinks() {
  return (
    <div className="hidden md:flex gap-6 text-sm font-medium text-gray-900 dark:text-white">
      <div className="flex space-x-4">
        <Link
          to="/"
          className="rounded-md bg-gray-900 text-white dark:bg-gray-800 px-3 py-2 text-sm font-medium"
        >
          Home
        </Link>

        <Link
          to="/posts"
          className="rounded-md px-3 py-2 text-sm font-medium text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-white/10"
        >
          Posts
        </Link>

        <Link
          to="/about"
          className="rounded-md px-3 py-2 text-sm font-medium text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-white/10"
        >
          About us
        </Link>
      </div>
    </div>
  );
}

export { NavLinks };
