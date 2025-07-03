import { useEffect, useState } from "react";
import ReportCard from "./components/ReportCard";
import './App.css';

function App() {
  const [theme, setTheme] = useState(() =>
    localStorage.getItem("theme") || "light"
  );

  const [data, setData] = useState({
    articles: [],
    loading: true,
    error: null,
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () =>
    setTheme((prev) => (prev === "light" ? "dark" : "light"));

  useEffect(() => {
    fetch("/api/reports")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((responseData) => {
        setData({
          articles: responseData.articles || [],
          loading: false,
          error: null,
        });
      })
      .catch((error) => {
        setData({
          articles: [],
          loading: false,
          error: error.message,
        });
      });
  }, []);

  if (data.loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-gray-50 dark:bg-gray-900">
        <p className="text-lg text-gray-600 dark:text-gray-300">
          Loading articles...
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white">
      {/* Sticky Header */}
      <header className="sticky top-0 z-10 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm px-6 py-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold">🛡️ Cybersecurity News</h1>
        <button
          onClick={toggleTheme}
          className="text-sm px-3 py-1 rounded bg-gray-200 dark:bg-gray-700 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600 transition"
        >
          Toggle {theme === "light" ? "Dark" : "Light"}
        </button>
      </header>

      <main className="container mx-auto px-6 py-8">
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {data.articles.map((article, index) => (
            <ReportCard key={article.id || index} article={article} />
          ))}
        </div>

        <div className="mt-10 text-center text-gray-500 dark:text-gray-400 italic">
          Total articles: {data.articles.length}
        </div>
      </main>
    </div>
  );
}

export default App;
