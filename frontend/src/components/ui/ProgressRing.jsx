import React from 'react';

export default function ProgressRing({
  percentage = 0,
  size = 80,
  strokeWidth = 7,
  color = '#6366F1',
  trackColor = 'rgba(255, 255, 255, 0.08)',
  label,
  subtitle
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const validPercentage = Math.min(Math.max(percentage, 0), 100);
  const strokeDashoffset = circumference - (validPercentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="rotate-[-90deg]">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={trackColor}
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            style={{ transition: 'stroke-dashoffset 0.8s ease' }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-sm font-extrabold text-white">{Math.round(validPercentage)}%</span>
        </div>
      </div>
      {label && <span className="text-xs font-semibold text-slate-300 mt-1.5 text-center">{label}</span>}
      {subtitle && <span className="text-[11px] text-slate-400 text-center">{subtitle}</span>}
    </div>
  );
}
