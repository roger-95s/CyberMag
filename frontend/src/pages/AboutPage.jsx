import Header from "../components/Header";

function About() {

    return (
        <>
            <div className="min-h-screen bg-white dark:bg-[#0a0f1a] text-gray-900 dark:text-gray-100 transition-colors duration-500">
                <Header />

                <div className="container mx-auto p-6 max-w-4xl">
                    {/* Hero Title */}
                    <h1 className="text-4xl font-extrabold mb-6 text-center">
                        About CyberMag
                    </h1>

                    {/* Marketing Section */}
                    <p className="text-lg mb-4 leading-relaxed">
                        CyberMag is a next-generation cybersecurity intelligence platform powered entirely by open-source AI technologies.
                        Our mission is to make cybersecurity insights accessible, transparent, and AI-driven — using modern models such as
                        <strong> Gemma 3</strong>, <strong>Llama 3.2</strong>, and <strong>DeepSeek-R1</strong> through the Ollama framework.
                    </p>

                    <p className="text-lg mb-4 leading-relaxed">
                        CyberMag was created to demonstrate what’s possible when innovation, open-source tools,
                        and modern engineering come together. The project showcases real full-stack development using two of the most
                        influential languages in the industry today: <strong>Python</strong> and <strong>JavaScript</strong>.
                    </p>

                    <p className="text-lg mb-4 leading-relaxed">
                        Our platform is built by a team of cybersecurity learners, seasoned engineers, and technology enthusiasts.
                        We are united by the belief that education, transparency, and community-driven knowledge can empower the next generation
                        of cybersecurity professionals.
                    </p>

                    <p className="text-lg mb-4 leading-relaxed">
                        CyberMag is still evolving. Features may be experimental, and some AI-generated content may include inaccuracies or
                        limitations. All information should be used for educational and informational purposes only.
                        We encourage users to validate findings and explore responsibly.
                    </p>

                    <p className="text-lg mb-10 leading-relaxed">
                        As we continue to grow, our focus remains on improving the platform, refining AI tools, and expanding our intelligence coverage.
                        We welcome feedback, collaboration, and innovation from our community.
                    </p>

                    <h2 className="text-3xl font-bold mb-6 text-center">Meet the CyberMag Team</h2>

                    {/* TEAM CARD GRID */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">

                        {/* Roger */}
                        <div className="bg-white/60 dark:bg-[#101726] border border-gray-200 dark:border-gray-700 rounded-xl shadow-md p-6 hover:shadow-xl transition-all duration-300">
                            <h3 className="text-xl font-semibold mb-1">Roger Campo</h3>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                                Software & Cloud Engineer · Co-Founder
                            </p>
                            <p className="text-md mb-4 leading-relaxed">
                                Software & Cloud Engineer with experience in IT support, security, AWS, Python, JavaScript, C, and SQL.
                                Certified in Computer Science and Web Programming, currently pursuing AWS AI Practitioner.
                                Passionate about secure development, problem-solving, and building meaningful technology.
                            </p>
                            <a
                                href="https://www.linkedin.com/in/roger-campo/"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:underline font-medium"
                            >
                                LinkedIn Profile →
                            </a>
                        </div>

                        {/* Cesar */}
                        <div className="bg-white/60 dark:bg-[#101726] border border-gray-200 dark:border-gray-700 rounded-xl shadow-md p-6 hover:shadow-xl transition-all duration-300">
                            <h3 className="text-xl font-semibold mb-1">César Tomedes</h3>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                                Senior Full-Stack Developer · Co-Founder
                            </p>
                            <p className="text-md mb-4 leading-relaxed">
                                Full-stack developer with 12+ years of experience in Laravel, Vue.js, and large-scale e-commerce solutions.
                                Expert in RESTful APIs, custom module development, WordPress architecture, MySQL optimization, and UI components.
                                Skilled in agile methodologies and modern DevOps practices.
                            </p>
                            <a
                                href="https://www.linkedin.com/in/c%C3%A9sar-tomedes-6b2688178/"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:underline font-medium"
                            >
                                LinkedIn Profile →
                            </a>
                        </div>

                    </div>

                    {/* Closing Message */}
                    <p className="text-center text-lg mt-10">
                        Thank you for visiting CyberMag. Where open-source innovation meets cybersecurity intelligence.
                    </p>
                </div>
            </div>
        </>

    );
}

export default About;