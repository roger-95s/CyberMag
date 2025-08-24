import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

export default function ReportPage() {
  const { id } = useParams(); // obtiene el post_id de la URL
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await fetch(`/post/${id}`);
        const data = await res.json();
        if (data.success) {
          setReport(data.article);
        } else {
          setError(data.error || "Report not found");
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [id]);

  if (loading) {
    return <p className="text-gray-500 p-4">Loading report...</p>;
  }

  if (error) {
    return <p className="text-red-500 p-4">{error}</p>;
  }

  if (!report) {
    return <p className="text-gray-500 p-4">No report found.</p>;
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">{report.title}</h1>
      <p className="text-gray-700 mb-4">{report.summary}</p>
      <span
        className={`inline-block px-3 py-1 rounded-full text-white mb-4 ${
          report.risk_level === "high"
            ? "bg-red-500"
            : report.risk_level === "medium"
            ? "bg-yellow-500"
            : report.risk_level === "low"
            ? "bg-green-500"
            : "bg-gray-400"
        }`}
      >
        {report.risk_level}
      </span>
      <div>
        <a
          href={report.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 underline"
        >
          Read full article
        </a>
      </div>
    </div>
  );
}
