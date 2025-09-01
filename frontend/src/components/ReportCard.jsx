import React, { useState } from "react";
import { ShieldCheck, Lock, Globe, BrainCircuit, Bug } from "lucide-react";

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

  const risk = articleData.risk_level?.toLowerCase() || "unknown";
  const riskColorClass = riskColors[risk] || riskColors["unknown"];

  const fetchAnalysis = async () => {
    setLoadingAnalysis(true);
    setError(null);
    try {
      const res = await fetch("/analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: articleData.url }),
      });
      if (!res.ok) throw new Error(`Status ${res.status}`);
      const data = await res.json();
      if (data.success) {
        setAnalysis(data.analysis?.[0] || null);
      } else {
        setError("Failed to get analysis");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingAnalysis(false);
    }
  };


  return (
    <div className="group relative rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm p-5 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ease-in-out">
      {/* Nueva estructura de cabecera: dos columnas */}
      <div className="flex items-start gap-4 mb-4">
        {/* Ícono a la izquierda */}
        <div className="flex-shrink-0">{icon}</div>

        {/* Fecha y título a la derecha */}
        <div className="flex flex-col">
          {/* Fecha del artículo */}
          {articleData.date && (
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
              {articleData.date}
            </p>
          )}

          {/* Título */}
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
            {/* <ShieldAlert className="w-5 h-5 text-blue-600 dark:text-blue-400" /> */}
            {articleData.url ? (
              <a
                href={articleData.url}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
              >
                {articleData.title}
              </a>
            ) : (
              articleData.title
            )}
          </h2>
        </div>
      </div>

      {/* Contenido: resumen y análisis */}
      <div className="text-sm mb-4">
        <p className="text-gray-600 dark:text-gray-300 mb-2 leading-relaxed">
          <strong>Summary:</strong>{" "}
          {articleData.summary ? (
            articleData.summary
          ) : (
            <span className="italic text-gray-400 dark:text-gray-500">
              No summary available.
            </span>
          )}
        </p>
      </div>

      {/* Pie: nivel de riesgo + análisis */}
      <div className="flex items-center justify-between mt-4">
        <span
          className={`px-3 py-1 rounded-full text-xs font-medium ${riskColorClass}`}
        >
          {/* peque~o cambio realizado para evitar que diga undefined si algun dato falla, se agrego ?? al fallback*/}
          Risk Level: {articleData.risk_level ?? "Unknown"}
        </span>
        <button
          onClick={fetchAnalysis}
          disabled={loadingAnalysis}
          className="ml-4 text-sm text-blue-500 hover:underline disabled:text-gray-400"
        >
          {loadingAnalysis ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-500">
          Error fetching analysis: {error}
        </p>
      )}

        {/* I'm seeing the this article.content, but I don't quat yet understand why we have this here?
          Waht I mean's I know that this work to show more content, but from where the content will come from?*/}
        {articleData.analysis_url ? (
          <a
            href={articleData.analysis_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-blue-500 hover:underline"
          >
            View full AI-generated analysis
          </a>
        ) : articleData.analysis ? (
          <span className="text-sm italic text-gray-500 dark:text-gray-400">
            {articleData.analysis}
          </span>
        ) : null}
      </div>
  );
}

export default ReportCard;
