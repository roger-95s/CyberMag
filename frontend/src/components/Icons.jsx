import { ShieldCheck, Lock, Globe, BrainCircuit, Bug } from "lucide-react";
// Icon map based on item type
const iconMap = {
    ai: <BrainCircuit className="w-10 h-10 text-cyan-400" />,
    threats: <ShieldCheck className="w-10 h-10 text-cyan-400" />,
    ransomware: <Bug className="w-10 h-10 text-purple-400" />,
    network: <Lock className="w-10 h-10 text-cyan-400" />,
    globe: <Globe className="w-10 h-10 text-cyan-400" />,
};

export { iconMap };