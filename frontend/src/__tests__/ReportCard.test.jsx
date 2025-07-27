import React from "react";
import { render, screen } from "@testing-library/react";
import ReportCard from "../components/ReportCard";

const mockArticle = {
  id: 1,
  icon: "ai",
  title: "Test Article",
  summary: "This is a test summary.",
  analysis: "Test analysis content.",
  riskLevel: "Medium",
  url: "https://example.com",
  type: "threats",
};

test("renderiza la tarjeta con título, resumen y análisis", () => {
  render(<ReportCard articleData={mockArticle} />);
  expect(screen.getByText(/test article/i)).toBeInTheDocument();
  expect(screen.getByText(/this is a test summary/i)).toBeInTheDocument();
  expect(screen.getByText(/test analysis content/i)).toBeInTheDocument();
});
