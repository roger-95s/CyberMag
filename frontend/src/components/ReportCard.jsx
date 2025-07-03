import React from "react";

const getRiskBadge = (level) => {
  if (!level) return "⚪ Unknown";

  switch (level.toLowerCase()) {
    case "critical":
      return "🔴 Critical";
    case "high":
      return "🟠 High";
    case "moderate":
    case "medium":
      return "🟡 Moderate";
    case "low":
      return "🟢 Low";
    default:
      return "⚪ Unknown";
  }
};

const ReportCard = ({ article }) => {
  return (
    <div className="border border-gray-300 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
      <h2 className="text-xl font-semibold mb-2">
        {article.url ? (
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 hover:underline"
          >
            {article.title || "Untitled Report"}
          </a>
        ) : (
          article.title || "Untitled Report"
        )}
      </h2>

      {/* Summary */}
      <p className="text-gray-700 mb-2">
        <strong>Summary:</strong>{" "}
        {article.summary || (
          <span className="italic text-gray-400">
            We’re working on the implementation of [Summary].
          </span>
        )}
      </p>

      {/* Analysis */}
      <p className="text-gray-700 mb-2">
        <strong>Analysis:</strong>{" "}
        {article.analysis || (
          <span className="italic text-gray-400">
            We’re working on the implementation of [Analysis].
          </span>
        )}
      </p>

      {/* Risk Level */}
      <p className="mb-2">
        <strong>Risk Level:</strong>{" "}
        <span className="inline-block bg-gray-100 px-2 py-1 rounded text-sm font-medium">
          {getRiskBadge(article.risk_level)}
        </span>
      </p>

      {/* Full Content */}
      {article.content && (
        <details className="mt-2">
          <summary className="cursor-pointer text-blue-600 hover:text-blue-800">
            Show Content
          </summary>
          <div className="mt-2 p-2 bg-gray-50 rounded text-sm">
            {article.content.substring(0, 500)}
            {article.content.length > 500 && "…"}
          </div>
        </details>
      )}
    </div>
  );
};

export default ReportCard;
