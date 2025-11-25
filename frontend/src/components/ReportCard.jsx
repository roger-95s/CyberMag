// "use client"; // Note: This directive should typically be at the very top of the file.

import { useState, useEffect } from "react";
import { ShieldCheck, Lock, Globe, BrainCircuit, Bug, Loader2 } from "lucide-react";
import { Link } from "react-router-dom";
import { HoverBorderGradient } from "./ui/HoverBorderGradiente"; // Assuming this is a local component

// --- Icon and Color Maps ---

// Icon map based on item type
const iconMap = {
  ai: <BrainCircuit className="w-10 h-10 text-cyan-400" />,
  threats: <ShieldCheck className="w-10 h-10 text-cyan-400" />,
  ransomware: <Bug className="w-10 h-10 text-purple-400" />,
  network: <Lock className="w-10 h-10 text-cyan-400" />,
  globe: <Globe className="w-10 h-10 text-cyan-400" />,
  unknown: <ShieldCheck className="w-10 h-10 text-cyan-400" />, // Default icon for "unknown"
};

// Color map according to risk level
const riskColors = {
  critical: "bg-red-500", // Using solid colors for the indicator dot
  high: "bg-orange-500",
  medium: "bg-yellow-500",
  low: "bg-green-500",
  unknown: "bg-gray-500",
  // Tooltip colors are kept as before for rich text
  critical_tooltip: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
  high_tooltip: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
  medium_tooltip: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
  low_tooltip: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
  unknown_tooltip: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-400",
};

// --- Individual Report Card Component ---

/**
 * Renders a single report card based on an article object.
 * @param {object} article - The article data object from the backend.
 */
function ReportCardItem({ article }) {
  // Sanitize and lookup values
  const icon = iconMap[article.icon] || iconMap.unknown;
  const risk = article.risk_level?.toLowerCase() || "unknown";
  const riskColorDot = riskColors[risk] || riskColors.unknown;
  const riskColorClass = riskColors[`${risk}_tooltip`] || riskColors.unknown_tooltip;

  // Use article.id for the dynamic link, fallback to a unique key if needed
  const articleId = article.id || article.title.replace(/\s/g, '-').toLowerCase();

  return (
    // Wrapper HoverBorderGradient for the entire card
    <HoverBorderGradient
      as="div"
      containerClassName="relative w-full max-w-[500px]"
      className={`
                rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700
                shadow-sm p-6 transition-all duration-400 ease-out
                hover:-translate-y-1 hover:shadow-[0_0_25px_rgba(0,255,255,0.2)]
            `}
    >
      {/* Header: Icon + title + risk indicator */}
      <div className="flex justify-between items-start mb-6">
        {/* Icon + text */}
        <div className="flex items-start gap-5">
          <div className="flex-shrink-0">{icon}</div>

          <div className="flex flex-col">
            {/* Note: The backend data doesn't provide a 'date', so I'm removing the date element
                         * for now, or you could add a fallback date if necessary. */}
            {/* {article.date && (
                            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                                {article.date}
                            </p>
                        )} */}

            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-50 leading-snug">
              <Link
                to={`/report/${articleId}`}
                className="hover:underline text-blue-600 dark:text-blue-400"
              >
                {article.title ?? "Untitled Article"}
              </Link>
            </h2>
          </div>
        </div>

        {/* Risk indicator converted to color + tooltip */}
        <div className="relative group/tooltip">
          <span
            className={`
                            w-3.5 h-3.5 rounded-full
                            animate-pulse cursor-pointer block
                            ${riskColorDot}
                        `}
          ></span>

          {/* Tooltip */}
          <div
            className={`
                            absolute right-0 top-6 opacity-0 group-hover/tooltip:opacity-100
                            transition-all duration-300 pointer-events-none
                            text-xs py-1 px-2 rounded-md shadow-lg z-10 whitespace-nowrap
                            ${riskColorClass}
                        `}
          >
            Risk Level: {article.risk_level ?? "Unknown"}
          </div>
        </div>
      </div>

      {/* Summary */}
      <p className="text-[15px] text-gray-700 dark:text-gray-300 leading-relaxed mb-6">
        <strong>Summary:</strong>{" "}
        {article.summary && article.summary !== "No Summary" ? (
          article.summary
        ) : (
          <span className="italic text-gray-400 dark:text-gray-500">
            [No summary from backend]
          </span>
        )}
      </p>

      {/* Footer: Learn More + button */}
      <div className="flex items-center justify-between mt-4">
        <Link
          to={`/report/${articleId}`}
          className="
                        group/learn relative flex items-center text-blue-500 text-sm font-medium 
                        whitespace-nowrap overflow-hidden
                    "
        >
          {/* Hidden text before hover */}
          <span
            className="
                        max-w-0 opacity-0 
                        group-hover/learn:max-w-[200px] group-hover/learn:opacity-100
                        transition-all duration-300 ease-out whitespace-nowrap
                        "
          >
            Learn more
          </span>

          {/* Arrow */}
          <span
            className="
                        text-lg ml-1 transition-transform duration-300
                        group-hover/learn:translate-x-1
                        "
          >
            →
          </span>
        </Link>

        {/* Button + (Optional: Could be used for saving/bookmarking) */}
        <button
          className="
                        w-9 h-9 flex items-center justify-center text-lg rounded-full
                        border border-gray-400 dark:border-gray-600
                        hover:bg-gray-200 dark:hover:bg-gray-700 transition
                    "
          aria-label="Save report"
        >
          +
        </button>
      </div>
    </HoverBorderGradient>
  );
}

// --- Main List Component ---

/**
 * Fetches and renders a list of ReportCardItems.
 */
export function ReportCardList() {
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setIsLoading(true);
    // Ensure you are using the correct API route: /api/posts from your Flask code
    fetch(`/api/posts`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((responseData) => {
        // The response is { articles_data: [article, ...], success: true, message: "..." }
        if (responseData.success && Array.isArray(responseData.articles_data)) {
          setArticles(responseData.articles_data);
          setError(null);
        } else {
          throw new Error("Invalid data format received from server.");
        }
      })
      .catch((err) => {
        setError(err.message);
        setArticles([]);
        console.error("Fetch Error:", err);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  return (
    <div className="space-y-6 max-w-4xl mx-auto py-10">
      <h1 className="text-3xl font-bold text-center text-gray-900 dark:text-gray-50">
        Latest CyberMag Reports
      </h1>

      {isLoading && (
        <div className="flex justify-center items-center h-48">
          <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          <span className="ml-3 text-lg text-gray-500">Loading Reports...</span>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-300 rounded-lg">
          <p className="font-semibold">Error fetching data:</p>
          <p>{error}</p>
        </div>
      )}

      {!isLoading && !error && articles.length === 0 && (
        <div className="p-4 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-300 rounded-lg">
          <p>No articles found.</p>
        </div>
      )}

      {!isLoading && articles.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {articles.map((article, index) => (
            <ReportCardItem key={article.id || index} article={article} />
          ))}
        </div>
      )}
    </div>
  );
}

export default ReportCardList;