import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ReportPage from "./pages/ReportPage";

function App() {
  return (
    <Router basename="/CyberMag">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/post/:id" element={<ReportPage />} />
        <Route
          path="*"

        />
      </Routes>
    </Router>
  );
}

export default App;
