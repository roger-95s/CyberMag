import React from "react";
import {
  ShieldCheck,
  Lock,
  Globe,
  BrainCircuit,
  Bug,
  FileText,
} from "lucide-react";

// Icon map based on item type
const iconMap = {
  ai: <BrainCircuit className="w-10 h-10 text-cyan-400" />,
  threats: <ShieldCheck className="w-10 h-10 text-cyan-400" />,
  ransomware: <Bug className="w-10 h-10 text-purple-400" />,
  network: <Lock className="w-10 h-10 text-cyan-400" />,
  globe: <Globe className="w-10 h-10 text-cyan-400" />,
};

// Color map according to risk level
const riskColors = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
  medium:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
  unknown: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-400",
};

function ReportCard({ article }) {
  const icon = iconMap[article.icon] || (
    <ShieldCheck className="w-10 h-10 text-cyan-400" />
  );

  const risk = article.risk_level?.toLowerCase() || "unknown";
  const riskColorClass = riskColors[risk] || riskColors["unknown"];

  return (
    <div className="group relative rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm p-5 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ease-in-out space-y-4">
      {/* Header: icon and content in 2 column */}
      <div className="grid grid-cols-[auto,1fr] items-center gap-4">
        {/* centered icon */}
        <div className="flex justify-center items-center w-14">{icon}</div>

        {/* date + title */}
        <div className="flex flex-col gap-1">
          <span className="text-sm text-gray-400 dark:text-gray-500">
            {article.date || "Unknown date"}
          </span>
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200 leading-snug">
            {article.url ? (
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
              >
                {article.title}
              </a>
            ) : (
              article.title
            )}
          </h2>
        </div>
      </div>

      {/* Summary visually aligned with the content */}
      <div className="ml-14">
        <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
          <strong>Summary:</strong>{" "}
          {article.summary ? (
            article.summary
          ) : (
            <span className="italic text-gray-400 dark:text-gray-500">
              No summary available.
            </span>
          )}
        </p>
      </div>
      {/* Buttons: right aligned */}
      <div className="flex items-center justify-end gap-4">
        <span
          className={`px-3 py-1 rounded-full text-xs font-medium ${riskColorClass}`}
        >
          Risk: {article.risk_level || "Unknown"}
        </span>
        {/* I'm seeing the this article.content, but I don't quat yet understand why we have this here?
          Waht I mean's I know that this work to show more content, but from where the content will come from?*/}
        {article.analysis && (
          <details className="text-sm text-blue-500 cursor-pointer group-open:text-blue-700">
            <summary className="list-none hover:underline flex items-center gap-1">
              <FileText className="w-4 h-4" />
              Analysis
            </summary>
            <div className="mt-2 text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 p-2 rounded text-sm max-w-md">
              {article.analysis.substring(0, 400)}
              {article.analysis.length > 400 && "..."}
            </div>
          </details>
        )}
      </div>
    </div>
  );
}

export default ReportCard;
