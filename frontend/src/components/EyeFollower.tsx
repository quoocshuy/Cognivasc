import { useEffect, useRef, useState } from "react";

interface EyeFollowerProps {
  size?: "small" | "medium" | "large";
  className?: string;
}

export const EyeFollower = ({ size = "medium", className = "" }: EyeFollowerProps) => {
  const eyeRef = useRef<HTMLDivElement>(null);
  const [pupilPosition, setPupilPosition] = useState({ x: 50, y: 50 });

  const sizeClasses = {
    small: "w-16 h-16",
    medium: "w-24 h-24",
    large: "w-48 h-48",
  };

  const pupilSizes = {
    small: "w-6 h-6",
    medium: "w-9 h-9",
    large: "w-20 h-20",
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!eyeRef.current) return;

      const eye = eyeRef.current;
      const eyeRect = eye.getBoundingClientRect();
      const eyeCenterX = eyeRect.left + eyeRect.width / 2;
      const eyeCenterY = eyeRect.top + eyeRect.height / 2;

      const angle = Math.atan2(e.clientY - eyeCenterY, e.clientX - eyeCenterX);
      const distance = Math.min(
        Math.sqrt(
          Math.pow(e.clientX - eyeCenterX, 2) + Math.pow(e.clientY - eyeCenterY, 2)
        ),
        eyeRect.width / 4
      );

      const maxDistance = eyeRect.width / 4;
      const normalizedDistance = (distance / maxDistance) * 35;

      const x = 50 + Math.cos(angle) * normalizedDistance;
      const y = 50 + Math.sin(angle) * normalizedDistance;

      setPupilPosition({ x, y });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div
      ref={eyeRef}
      className={`${sizeClasses[size]} ${className} relative rounded-full bg-white shadow-medium border-4 border-primary/20 overflow-hidden`}
    >
      {/* Sclera (white part) */}
      <div className="absolute inset-0 bg-gradient-to-br from-white to-secondary/30" />
      
      {/* Iris */}
      <div
        className="absolute rounded-full transition-all duration-100 ease-out"
        style={{
          width: size === "large" ? "60%" : "55%",
          height: size === "large" ? "60%" : "55%",
          left: `${pupilPosition.x}%`,
          top: `${pupilPosition.y}%`,
          transform: "translate(-50%, -50%)",
          background: "radial-gradient(circle at 30% 30%, hsl(195 70% 60%), hsl(195 85% 40%), hsl(195 90% 25%))",
        }}
      >
        {/* Pupil */}
        <div
          className={`${pupilSizes[size]} absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-to-br from-gray-900 to-black`}
        >
          {/* Light reflection */}
          <div className="absolute top-2 left-2 w-2 h-2 rounded-full bg-white/80" />
        </div>
      </div>

      {/* Eye shine */}
      <div className="absolute top-2 right-2 w-4 h-4 rounded-full bg-white/40 blur-sm" />
    </div>
  );
};
