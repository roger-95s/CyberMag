import Header from "../components/Header";
import Hero from "../components/Hero"
import ReportCard from "../components/ReportCard"



function HomePage() {

  fetch(`/api/home`)
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      return res.json();
    })
    .then((responseData) => {
    })
    .catch((error) => {

    }, []);

  return (
    <div className="min-h-screen bg-white dark:bg-[#0a0f1a] text-gray-900 dark:text-gray-100 transition-colors duration-500">
      <Header />
      <Hero />
      <div className="container mx-auto p-4">
        <ReportCard />
      </div>
    </div>
  );
}

export default HomePage;