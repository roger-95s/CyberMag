import { useState, useEffect } from "react";
import ReportCard from "./components/ReportCard";
import './App.css';

function App() {
  const [data, setData] = useState({
    articles: [],
    loading: true,
    error: null
  });

  useEffect(() => {
    fetch("/api/reports")
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(responseData => {
        setData({
          articles: responseData.articles || [],
          loading: false,
          error: null
        });
      })
      .catch(error => {
        setData({
          articles: [],
          loading: false,
          error: error.message
        });
      });
  }, []);

  if (data.loading) {
    return (
<div className="p-4 space-y-4">
    <div className="bg-green-100 text-green-800 p-4 rounded">
      Tailwind CSS está funcionando correctamente 🎉
    </div>
    <p>Loading articles...</p>
  
    </div>
    
    );
  }

  if (data.error) {
    return (
      <div className="p-4">
        <p className="text-red-500">Error: {data.error}</p>
      </div>
    );
  }

  if (data.articles.length === 0) {
    return (
      <div className="p-4">
        <p>No articles found.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Cybersecurity News</h1>
      <div className="space-y-4">
        {data.articles.map((article, index) => (
          <ReportCard key={article.id || index} article={article} />
        ))}
      </div>
      <div className="mt-6 text-center text-gray-500">
        Total articles: {data.articles.length}
      </div>
    </div>
    
    
  ); 
}


export default App;
