import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, Sparkles, Target, Zap, ShieldCheck } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { profileAPI, systemAPI } from '../../services/api';

export default function Navbar({ onToggleSidebar }) {
  const { user } = useAuth();
  const [targetCareer, setTargetCareer] = useState('AI/ML Engineer');
  const [llmStatus, setLlmStatus] = useState({ configured: false, provider: 'gemini' });

  useEffect(() => {
    const fetchNavbarData = async () => {
      try {
        const [profRes, healthRes] = await Promise.allSettled([
          profileAPI.getProfile(),
          systemAPI.getHealth()
        ]);
        if (profRes.status === 'fulfilled' && profRes.value.data.target_career) {
          setTargetCareer(profRes.value.data.target_career);
        }
        if (healthRes.status === 'fulfilled') {
          setLlmStatus({
            configured: healthRes.value.data.llm_configured,
            provider: healthRes.value.data.llm_provider
          });
        }
      } catch (e) {
        console.error("Navbar data fetch error", e);
      }
    };
    fetchNavbarData();
  }, []);

  return (
    <header className="sticky top-0 z-30 h-16 bg-[#090D16]/80 backdrop-blur-md border-b border-white/8 flex items-center justify-between px-4 lg:px-8">
      {/* Left: Mobile Toggle & Page Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-xl lg:hidden transition-colors"
          aria-label="Toggle Navigation"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="hidden sm:flex items-center gap-2">
          <NavLink
            to="/career-analysis"
            className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-xs font-semibold text-indigo-300 hover:bg-indigo-500/20 transition-colors"
          >
            <Target className="w-3.5 h-3.5 text-indigo-400" />
            <span>Target: <span className="text-white font-bold">{targetCareer}</span></span>
          </NavLink>
        </div>
      </div>

      {/* Right: AI Provider Pill & User Pill */}
      <div className="flex items-center gap-3">
        {/* AI Engine Status Pill */}
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[11px] font-medium text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>{llmStatus.configured ? 'Google Gemini Online' : 'AI Grounded Engine'}</span>
        </div>

        {/* Profile Pill */}
        <NavLink
          to="/profile"
          className="flex items-center gap-2.5 pl-2 pr-3 py-1 rounded-full glass-panel hover:border-indigo-500/40 transition-colors"
        >
          <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center text-xs font-bold text-white shadow-sm">
            {user?.full_name?.charAt(0) || 'R'}
          </div>
          <span className="text-xs font-semibold text-slate-200 hidden md:inline">
            {user?.full_name?.split(' ')[0] || 'Rahul'}
          </span>
        </NavLink>
      </div>
    </header>
  );
}
