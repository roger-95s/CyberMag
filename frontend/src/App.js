import { useState, useEffect } from "react";
import ReportCard from "./components/ReportCard";
import Header from "./components/Header";
import Hero from "./components/Hero";
import "./App.css";

function App() {
  const [data, setData] = useState({
    articles_data: [],
    loading: true,
    error: null,
  });

  useEffect(() => {
    fetch("/api/index")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((responseData) => {
        setData({
          articles_data: responseData.articles_data || [],
          loading: false,
          error: null,
        });
      })
      .catch((error) => {
        setData({
          articles_data: [],
          loading: false,
          error: error.message,
        });
      });
  }, []);

  if (data.loading) {
    return (
      <>
        <Header />
        <Hero />
        <div className="p-4 space-y-4 bg-white text-gray-900 dark:bg-[#0a0f1a] dark:text-gray-100 min-h-screen transition-colors duration-500">
          <div className="bg-green-100 text-green-800 p-4 rounded"></div>
          <p>Loading articles...</p>
        </div>
      </>
    );
  }
  if (data.error) {
    return (
      <>
        <Header />
        <Hero />
        <div className="p-4 bg-white text-gray-900 dark:bg-[#0a0f1a] dark:text-gray-100 min-h-screen transition-colors duration-500">
          <p className="text-red-500">Error: {data.error}</p>
        </div>
      </>
    );
  }
  if (data.articles_data.length === 0) {
    return (
      <>
        <Header />
        <div className="p-4 bg-white text-gray-900 dark:bg-[#0a0f1a] dark:text-gray-100 min-h-screen transition-colors duration-500">
          <p>❌ No articles found.</p>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <Hero />
      <div className="min-h-screen bg-white text-gray-900 dark:bg-[#0a0f1a] dark:text-gray-100 transition-colors duration-500">
        <div className="container mx-auto p-4">
          <h1 className="text-3xl font-bold mb-6 text-center">
            Cybersecurity News
          </h1>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.articles_data.map((article, index) => (
              <ReportCard key={index} articleData={article} />
            ))}
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
