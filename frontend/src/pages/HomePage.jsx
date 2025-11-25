import { useState, useEffect } from "react";
import Header from "../components/Header";
import Hero from "../components/Hero"
import ReportCard from "../components/ReportCard"

function HomePage() {
  const [data, setData] = useState({
    message: "",
    articles_data: [],
    loading: true,
    error: null,

  });

  // Pagination state
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
        setTotalPages(responseData.total_pages || 1);
      })
      .catch((error) => {
        setData({
          message: "",
          articles_data: [],
          loading: false,
        });
      });
  }, [currentPage]);

  return (
    <div className="min-h-screen bg-white dark:bg-[#0a0f1a] text-gray-900 dark:text-gray-100 transition-colors duration-500">
      <Header />
      <Hero />
      <div className="container mx-auto p-4">
        <ReportCard />
      </div>

    </div>
  );
}

export default HomePage;