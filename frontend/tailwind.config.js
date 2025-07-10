// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  darkMode: "class",
  theme: {
    extend: {},
  },
  plugins: [
    // @tailwindcss/line-clamp is now built into Tailwind CSS v3.3+
    // No plugin needed - just use line-clamp-{n} classes directly
  ],
};
