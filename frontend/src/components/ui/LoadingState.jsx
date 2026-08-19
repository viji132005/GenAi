import React from 'react';
import { Sparkles } from 'lucide-react';

export default function LoadingState({ message = "AI Engine is analyzing your profile...", subtext = "Synthesizing career vectors and industry requirements" }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center min-h-[300px]">
      <div className="relative mb-6">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 to-cyan-400 animate-spin flex items-center justify-center p-0.5 shadow-lg shadow-indigo-500/30">
          <div className="w-full h-full bg-[#090D16] rounded-[14px]" />
        </div>
        <div className="absolute inset-0 flex items-center justify-center">
          <Sparkles className="w-7 h-7 text-indigo-400 animate-pulse" />
        </div>
      </div>
      <h3 className="text-lg font-bold font-heading text-white mb-1.5">{message}</h3>
      <p className="text-sm text-slate-400 max-w-sm">{subtext}</p>
    </div>
  );
}
