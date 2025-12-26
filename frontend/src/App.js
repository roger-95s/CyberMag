import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import PostPage from "./pages/PostPage";
import ReportPage from "./pages/ReportPage";
import About from "./pages/AboutPage";
import Footer from "./components/Footer";

function App() {
  //  PUBLIC_URL works both on localhost and in production without worrying about
  const basename = process.env.PUBLIC_URL;

  return (
    <Router basename={basename}>
      {/* routers */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/posts" element={<PostPage />} />
        <Route path="/about" element={<About />} />
        <Route path="/report/:id" element={<ReportPage />} />

        <Route
          path="*"
          element={<h2 className="text-center mt-10">404 - Not Found</h2>}
        />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
