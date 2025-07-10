import React from "react";
import {
  ShieldCheck,
  Lock,
  Globe,
  BrainCircuit,
  Bug,
  FileText,
} from "lucide-react";

// Mapa de íconos basado en el tipo de artículo
const iconMap = {
  ai: <BrainCircuit className="w-10 h-10 text-cyan-400" />,
  threats: <ShieldCheck className="w-10 h-10 text-cyan-400" />,
  ransomware: <Bug className="w-10 h-10 text-purple-400" />,
  network: <Lock className="w-10 h-10 text-cyan-400" />,
  globe: <Globe className="w-10 h-10 text-cyan-400" />,
};

// Mapa de colores según el nivel de riesgo
const riskColors = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
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
    <div className="group relative rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm p-5 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ease-in-out">
      {/* Ícono centrado */}
      <div className="flex justify-center mb-4">{icon}</div>

      {/* Título */}
      <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center gap-2">
        {/* <ShieldAlert className="w-5 h-5 text-blue-600 dark:text-blue-400" /> */}
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

      {/* Contenido: resumen y análisis */}
      <div className="text-sm mb-3">
        <p className="text-gray-600 dark:text-gray-300 mb-1 leading-relaxed line-clamp-3">
          <strong>Summary:</strong>{" "}
          {article.summary ? (
            article.summary
          ) : (
            <span className="italic text-gray-400 dark:text-gray-500">
              No summary available.
            </span>
          )}
        </p>
        <p className="text-gray-500 dark:text-gray-400 italic line-clamp-2">
          <strong>Analysis:</strong>{" "}
          {article.analysis ? (
            article.analysis
          ) : (
            <span className="italic text-gray-400 dark:text-gray-500">
              No analysis provided.
            </span>
          )}
        </p>
      </div>

      {/* Pie: nivel de riesgo + más contenido */}
      <div className="flex items-center justify-between">
        <span
          className={`px-3 py-1 rounded-full text-xs font-medium ${riskColorClass}`}
        >
          Risk Level: {article.risk_level || "Unknown"}
        </span>

        {article.content && (
          <details className="ml-auto text-sm text-blue-500 cursor-pointer group-open:text-blue-700">
            <summary className="list-none hover:underline flex items-center gap-1">
              <FileText className="w-4 h-4" />
              Show more
            </summary>
            <div className="mt-2 text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 p-2 rounded text-sm">
              {article.content.substring(0, 400)}
              {article.content.length > 400 && "..."}
            </div>
          </details>
        )}
      </div>
    </div>
  );
}

export default ReportCard;
