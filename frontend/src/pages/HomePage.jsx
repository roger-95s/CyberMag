import { useState, useEffect } from "react";
import Header from "../components/Header";
import Hero from "../components/Hero";
import ReportCard from "../components/ReportCard";
import "../App.css";

function HomePage() {
  const [data, setData] = useState({
    message: "",
    articles_data: [],
    loading: true,
    error: null,
  });

  // estados para el paginador
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const articlesPerPage = 9;

  useEffect(() => {
    setData((prev) => ({ ...prev, loading: true }));

    fetch(`/api/home?page=${currentPage}&limit=${articlesPerPage}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((responseData) => {
        setData({
          message: responseData.message || "Welcome to CyberMag!",
          articles_data: responseData.articles_data || [],
          loading: false,
          error: null,
        });

        //  Guarda total de páginas desde backend
        setTotalPages(responseData.total_pages || 1);
      })
      .catch((error) => {
        setData({
          message: "",
          articles_data: [],
          loading: false,
          error: error.message,
        });
      });
  }, [currentPage]); //  se volvera a ejecutar cuando cambie la página

  return (
    <div className="min-h-screen bg-white dark:bg-[#0a0f1a] text-gray-900 dark:text-gray-100 transition-colors duration-500">
      <Header />
      <Hero />

      <div className="container mx-auto p-4">
        {/* Loading */}
        {data.loading && (
          <p className="text-center text-lg font-medium text-gray-700 dark:text-gray-300">
            Loading articles...
          </p>
        )}

        {/* Error */}
        {data.error && (
          <p className="text-center text-lg font-medium text-red-500">
            Error: {data.error}
          </p>
        )}

        {/* Welcome message */}
        {!data.loading && !data.error && (
          <div className="text-center mb-6">
            <h2 className="text-2xl font-semibold">{data.message}</h2>
          </div>
        )}

        {/* Articles grid */}
        {!data.loading && !data.error && data.articles_data.length > 0 && (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.articles_data.map((article, index) => (
                <ReportCard key={index} articleData={article} />
              ))}
            </div>

            <div className="flex justify-center mt-8 space-x-2">
              {Array.from({ length: totalPages }, (_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentPage(index + 1)}
                  className={`px-4 py-2 rounded-md border text-sm font-medium transition-colors
                    ${
                      currentPage === index + 1
                        ? "bg-blue-600 text-white border-blue-600"
                        : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 border-gray-400 hover:bg-gray-300 dark:hover:bg-gray-600"
                    }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          </>
        )}

        {/* No articles */}
        {!data.loading && !data.error && data.articles_data.length === 0 && (
          <p className="text-center text-lg font-medium text-gray-500">
            ❌ No articles found.
          </p>
        )}
      </div>
    </div>
  );
}

export default HomePage;
