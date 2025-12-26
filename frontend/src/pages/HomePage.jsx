import { useState, useEffect } from "react";
import Header from "../components/Header";
import Hero from "../components/Hero";
import Pagination from "../components/Pagination";
import { ReportCardItem } from "../components/ReportCard";

function HomePage() {
  const [allArticles, setAllArticles] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const articlesPerPage = 6;
  const handlePageChange = (page) => {
    setCurrentPage(page);

    // Scrolls down after re-rendering
    // Prevents the scroll bar from scrolling up when changing pages
    setTimeout(() => {
      window.scrollTo({
        top: document.body.scrollHeight, // Go to the end of the content
        behavior: "smooth", // Smooth animation
      });
    }, 0);
  };
  useEffect(() => {
    setLoading(true);
    setError(null);

    fetch(`/api/home?limit=1000`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        const articles = data.articles_data || data.articles || [];
        setAllArticles(articles);

        const pages = Math.max(1, Math.ceil(articles.length / articlesPerPage));
        setTotalPages(pages);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const startIndex = (currentPage - 1) * articlesPerPage;
  const visibleArticles = allArticles.slice(
    startIndex,
    startIndex + articlesPerPage
  );

  return (
    <div className="min-h-screen bg-white dark:bg-[#0a0f1a] text-gray-900 dark:text-gray-100 transition-colors duration-500">
      <Header />
      <Hero />

      {loading && <p className="text-center mt-4">Loading...</p>}
      {error && <p className="text-center mt-4 text-red-500">{error}</p>}

      {!loading && !error && (
        <>
          <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-50 text-center">
              Latest CyberMag Reports
            </h1>

            {visibleArticles.length === 0 ? (
              <p className="text-center text-gray-600 dark:text-gray-400">
                No articles found.
              </p>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {visibleArticles.map((article) => (
                  <ReportCardItem
                    key={article.id ?? article.title}
                    article={article}
                  />
                ))}
              </div>
            )}
          </div>

          <div className="container mx-auto p-4">
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          </div>
        </>
      )}
    </div>
  );
}

export default HomePage;
