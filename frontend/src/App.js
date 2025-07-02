import { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState({
    articles: [],
    loading: true,
    error: null
  });

  // Fetch the reports from API
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
        // console.log("Fetched data:", responseData);
      })
      .catch(error => {
        // console.error("Error fetching data:", error);
        setData({
          articles: [],
          loading: false,
          error: error.message
        });
      });
  }, []);

  // Loading state
  if (data.loading) {
    return (
      <div className="p-4">
        <p>Loading articles...</p>
      </div>
    );
  }

  // Error state
  if (data.error) {
    return (
      <div className="p-4">
        <p className="text-red-500">Error: {data.error}</p>
      </div>
    );
  }

  // No articles state
  if (data.articles.length === 0) {
    return (
      <div className="p-4">
        <p>No articles found.</p>
      </div>
    );
  }

  // Render articles
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Cybersecurity News</h1>
      <div className="space-y-4">
        {data.articles.map((article, index) => (
          <div key={article.id || index} className="border border-gray-300 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-xl font-semibold mb-2">
              {article.url ? (
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 hover:underline"
                >
                  {article.title}
                </a>
              ) : (
                article.title
              )}
            </h2>

            {article.summary && (
              <p className="text-gray-700 mb-2">{article.summary}</p>
            )}

            {article.risk_level && (
              <span className={`inline-block px-2 py-1 rounded text-sm font-medium ${article.risk_level.toLowerCase() === 'critical' ? 'bg-red-100 text-red-800' :
                  article.risk_level.toLowerCase() === 'high' ? 'bg-orange-100 text-orange-800' :
                    article.risk_level.toLowerCase() === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      article.risk_level.toLowerCase() === 'low' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                }`}>
                Risk: {article.risk_level}
              </span>
            )}

            {article.content && (
              <details className="mt-2">
                <summary className="cursor-pointer text-blue-600 hover:text-blue-800">
                  Show Content
                </summary>
                <div className="mt-2 p-2 bg-gray-50 rounded text-sm">
                  {article.content.substring(0, 500)}
                  {article.content.length > 500 && "..."}
                </div>
              </details>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 text-center text-gray-500">
        Total articles: {data.articles.length}
      </div>
    </div>
  );
}

export default App;
