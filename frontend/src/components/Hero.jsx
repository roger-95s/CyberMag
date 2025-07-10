import React, { useEffect, useState } from "react";
import { ShieldCheck } from "lucide-react";

const Hero = () => {
  const lines = React.useMemo(
    () => [
      "fetching cyber-intel...",
      "✔️ AI Threats detected",
      "✔️ Ransomware patterns updated",
      "✔️ Network firewalls active",
      "> Ready for new reports",
    ],
    []
  );

  const [displayedLines, setDisplayedLines] = useState([]);
  const [currentLine, setCurrentLine] = useState(0);
  const [currentChar, setCurrentChar] = useState(0);

  useEffect(() => {
    let timeout;

    if (currentLine < lines.length) {
      if (currentChar < lines[currentLine].length) {
        timeout = setTimeout(() => {
          setDisplayedLines((prev) => {
            const updated = [...prev];
            updated[currentLine] =
              (updated[currentLine] || "") + lines[currentLine][currentChar];
            return updated;
          });
          setCurrentChar((prev) => prev + 1);
        }, 30);
      } else {
        timeout = setTimeout(() => {
          setCurrentLine((prev) => prev + 1);
          setCurrentChar(0);
        }, 400);
      }
    } else {
      // Reiniciar animación luego de una pausa
      timeout = setTimeout(() => {
        setDisplayedLines([]);
        setCurrentLine(0);
        setCurrentChar(0);
      }, 2000);
    }

    return () => clearTimeout(timeout);
  }, [currentChar, currentLine, lines]);

  return (
    <section className="bg-white dark:bg-[#0a0f1a] text-gray-900 dark:text-white py-16 transition-colors duration-500">
      <div className="container mx-auto px-4 text-center">
        {/* Headline */}
        <h1 className="text-4xl sm:text-5xl font-bold mb-4">
          STAY AHEAD OF CYBER THREATS
        </h1>

        {/* Subheading */}
        <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
          Actionable insights and threat analysis for the evolving digital landscape.
        </p>

        {/* Icon */}
        <div className="flex justify-center mb-8">
          <ShieldCheck className="w-12 h-12 text-cyan-500 animate-pulse" />
        </div>

        {/* Terminal Block */}
        <div className="mt-4 max-w-2xl mx-auto bg-black text-green-400 font-mono text-sm rounded-lg overflow-hidden shadow-lg border border-gray-700">
          {/* Terminal Header */}
          <div className="bg-gray-800 px-4 py-2 flex items-center justify-between text-white text-xs">
            <span>cybermag@terminal:~$</span>
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-red-500 rounded-full" />
              <span className="w-2 h-2 bg-yellow-500 rounded-full" />
              <span className="w-2 h-2 bg-green-500 rounded-full" />
            </div>
          </div>

          {/* Animated Lines */}
          <div className="p-4 min-h-[140px]">
            {displayedLines.map((line, i) => (
              <p key={i} className={line.startsWith(">") ? "text-cyan-400" : ""}>
                {line}
              </p>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
