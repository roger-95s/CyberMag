"use client";

import { useState } from "react";
import { ShieldCheck, Lock, Globe, BrainCircuit, Bug } from "lucide-react";
import { Link } from "react-router-dom";
import { HoverBorderGradient } from "./ui/HoverBorderGradiente";
// import ReportCard from "./Postsreport";

// Icon map based on item type
const iconMap = {
  ai: <BrainCircuit className="w-10 h-10 text-cyan-400" />,
  threats: <ShieldCheck className="w-10 h-10 text-cyan-400" />,
  ransomware: <Bug className="w-10 h-10 text-purple-400" />,
  network: <Lock className="w-10 h-10 text-cyan-400" />,
  globe: <Globe className="w-10 h-10 text-cyan-400" />,
};

// Color map according to risk level (only used for tooltip now) 
const riskColors = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
  medium:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
  unknown: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-400",
};

function ReportCard({ articleData }) {
  const [analysis, setAnalysis] = useState(null);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);
  const [error, setError] = useState(null);

  const icon = iconMap[articleData.icon] || (
    <ShieldCheck className="w-10 h-10 text-cyan-400" />
  );

  const fetchAnalysis = async () => {
    setLoadingAnalysis(true);
    setError(null);
    try {
      const res = await fetch("/api/post", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: articleData.url }),
      });
      if (!res.ok) throw new Error(`Status ${res.status}`);
      const data = await res.json();
      if (!data.success) setError("Failed to get analysis");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingAnalysis(false);
    }
  };

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
      {/* Header: Icon + date + title + risk indicator */}
      <div className="flex justify-between items-start mb-6">
        {/* Icon + text */}
        <div className="flex items-start gap-5">
          <div className="flex-shrink-0">{icon}</div>

          <div className="flex flex-col">
            {articleData.date && (
              <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                {articleData.date}
              </p>
            )}

            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-50 leading-snug">
              <Link
                to={`/report/${articleData.id}`}
                className="hover:underline text-blue-600 dark:text-blue-400"
              >
                {articleData.title ?? "Untitled Article"}
              </Link>
            </h2>
          </div>
        </div>
        {/* Risk indicator converted to color + tooltip */}{" "}
        <div className="relative group/tooltip">
          <span
            className="
              w-3.5 h-3.5 rounded-full bg-gray-400 dark:bg-gray-500 
              animate-pulse cursor-pointer block
            "
          ></span>

          {/* Tooltip */}
          <div
            className="
              absolute right-0 top-6 opacity-0 group-hover/tooltip:opacity-100
              transition-all duration-300 pointer-events-none
              bg-black text-white text-xs py-1 px-2 rounded-md shadow-lg
            "
          >
            Risk Level: {articleData.risk_level ?? "Unknown"}
          </div>
        </div>
      </div>

      {/* Summary */}
      <p className="text-[15px] text-gray-700 dark:text-gray-300 leading-relaxed mb-6">
        <strong>Summary:</strong>{" "}
        {articleData.summary ? (
          articleData.summary
        ) : (
          <span className="italic text-gray-400 dark:text-gray-500">
            [No summary from backend]
          </span>
        )}
      </p>

      {/* Footer: Learn More + button + */}
      <div className="flex items-center justify-between mt-4">
        {/* Learn More → (animated and on a single line) */}
        <button
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
        </button>

        {/* Button + */}
        <button
          onClick={fetchAnalysis}
          disabled={loadingAnalysis}
          className="
            w-9 h-9 flex items-center justify-center text-lg rounded-full
            border border-gray-400 dark:border-gray-600
            hover:bg-gray-200 dark:hover:bg-gray-700 transition
          "
        >
          +
        </button>
      </div>

      {error && (
        <p className="mt-3 text-sm text-red-500">
          Error fetching analysis: {error}
        </p>
      )}
    </HoverBorderGradient>
  );
}

export default ReportCard;
