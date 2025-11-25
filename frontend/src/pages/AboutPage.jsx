import Header from "../components/Header";

function About() {

    return (
        <>
            <div className="min-h-screen bg-white dark:bg-[#0a0f1a] text-gray-900 dark:text-gray-100 transition-colors duration-500">
                <Header />
                <div className="container mx-auto p-6">
                    <h1 className="text-3xl font-bold mb-6">About CyberMag</h1>
                    <p className="text-lg mb-4">
                        CyberMag is a cutting-edge platform dedicated to providing the latest news, insights, and analysis on cybersecurity threats, trends, and technologies. Our mission is to empower individuals and organizations with the knowledge they need to stay safe in the digital world.
                    </p>
                    <p className="text-lg mb-4">
                        Founded in 2023, CyberMag has quickly become a trusted source for cybersecurity professionals, enthusiasts, and anyone interested in understanding the complexities of online security. Our team of expert writers and analysts work tirelessly to deliver accurate and timely information on a wide range of topics, from data breaches and malware to privacy concerns and regulatory developments.
                    </p>
                    <p className="text-lg mb-6">
                        At CyberMag, we believe that knowledge is power. By staying informed about the latest cybersecurity developments, our readers can make better decisions about how to protect themselves and their digital assets. Whether you're a seasoned IT professional or just starting to explore the world of cybersecurity, CyberMag has something for you.
                    </p>
                    <p className="text-lg">
                        Thank you for visiting CyberMag. We hope you find our content informative and engaging. If you have any questions or feedback, please don't hesitate to reach out to us.
                    </p>
                </div>
            </div>
        </>
    );
}

export default About;