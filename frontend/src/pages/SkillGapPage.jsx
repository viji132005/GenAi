import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  GitPullRequest,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ExternalLink,
  Clock,
  ArrowRight,
  BookOpen,
  Target
} from 'lucide-react';
import { skillsAPI, careerAPI } from '../services/api';
import ProgressRing from '../components/ui/ProgressRing';
import LoadingState from '../components/ui/LoadingState';

export default function SkillGapPage() {
  const [targetCareer, setTargetCareer] = useState('');
  const [careerList, setCareerList] = useState([]);
  const [gapData, setGapData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchSkillGaps = async (careerTitle) => {
    setLoading(true);
    try {
      const [gapRes, catRes] = await Promise.all([
        skillsAPI.analyzeSkillGaps(careerTitle),
        careerAPI.getCatalogs()
      ]);
      setGapData(gapRes.data);
      setTargetCareer(gapRes.data.career_title);
      setCareerList(catRes.data || []);
    } catch (e) {
      console.error('Error fetching skill gaps', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillGaps();
  }, []);

  const handleCareerChange = (newCareer) => {
    setTargetCareer(newCareer);
    fetchSkillGaps(newCareer);
  };

  if (loading && !gapData) {
    return <LoadingState message="Calculating skill gap matrix..." subtext="Comparing your current skill proficiencies against target industry requirements" />;
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header with Career Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold mb-2">
            <GitPullRequest className="w-3.5 h-3.5" />
            <span>AI Skill Gap Diagnostic Matrix</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            Skill Gap Analyzer
          </h1>
          <p className="text-sm text-slate-400">
            Compare your verified competencies against industry standards for your target role.
          </p>
        </div>

        {/* Career Selector Dropdown */}
        <div className="flex items-center gap-3">
          <label className="text-xs font-semibold text-slate-400 hidden sm:inline">Role:</label>
          <select
            value={targetCareer}
            onChange={(e) => handleCareerChange(e.target.value)}
            className="px-4 py-2.5 rounded-xl bg-[#111827] border border-white/10 text-white text-sm font-semibold focus:outline-none focus:border-indigo-500"
          >
            {careerList.map((c) => (
              <option key={c.title} value={c.title}>{c.title}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Overview Score Card */}
      <div className="p-6 rounded-3xl glass-panel border border-cyan-500/20 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 max-w-2xl text-center md:text-left">
          <span className="text-xs uppercase font-bold tracking-widest text-cyan-400">Strategic Diagnostic</span>
          <h3 className="text-lg font-bold font-heading text-white">
            {gapData?.high_priority_gaps?.length > 0
              ? `You have ${gapData.high_priority_gaps.length} high-priority skill gaps to bridge.`
              : 'You have solid foundation coverage for this career!'}
          </h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            {gapData?.recommended_action_plan}
          </p>
        </div>

        <div className="flex items-center gap-6 border-t md:border-t-0 md:border-l border-white/10 pt-4 md:pt-0 md:pl-6">
          <ProgressRing
            percentage={gapData?.overall_match_score || 78}
            size={76}
            strokeWidth={6}
            color="#06B6D4"
            label="Skill Match"
          />
        </div>
      </div>

      {/* The 3 Diagnostic Columns: Acquired, Partial, Missing */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* 1. ACQUIRED SKILLS */}
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-300">
                Acquired Skills ({gapData?.acquired_skills?.length || 0})
              </span>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">100% Fit</span>
          </div>

          <div className="space-y-3">
            {gapData?.acquired_skills?.map((item, idx) => (
              <div key={idx} className="p-4 rounded-2xl glass-panel border border-emerald-500/20 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm font-bold text-white">{item.skill_name}</span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300">
                      {item.current_proficiency}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400 block mb-2">{item.category}</span>
                </div>
                <div className="flex items-center gap-1 text-[11px] text-emerald-400 font-medium">
                  <CheckCircle2 className="w-3 h-3" /> Meets industry requirement ({item.required_proficiency})
                </div>
              </div>
            ))}
            {gapData?.acquired_skills?.length === 0 && (
              <p className="text-xs text-slate-500 text-center py-6">No matching acquired skills detected yet.</p>
            )}
          </div>
        </div>

        {/* 2. PARTIALLY DEVELOPED SKILLS */}
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/20">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-amber-300">
                Partially Developed ({gapData?.partial_skills?.length || 0})
              </span>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold">Upgrade Required</span>
          </div>

          <div className="space-y-3">
            {gapData?.partial_skills?.map((item, idx) => (
              <div key={idx} className="p-4 rounded-2xl glass-panel border border-amber-500/20 space-y-3">
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm font-bold text-white">{item.skill_name}</span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-amber-500/15 text-amber-300">
                      {item.current_proficiency} → {item.required_proficiency}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-[11px] text-slate-400">
                    <Clock className="w-3 h-3 text-amber-400" />
                    <span>Est. {item.estimated_weeks} weeks to advance</span>
                  </div>
                </div>

                {item.recommended_resources?.length > 0 && (
                  <div className="pt-2 border-t border-white/5 space-y-1.5">
                    <span className="text-[10px] uppercase tracking-wider font-bold text-slate-400 block">Recommended Resources:</span>
                    {item.recommended_resources.slice(0, 2).map((res, rIdx) => (
                      <a
                        key={rIdx}
                        href={res.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs text-indigo-400 hover:underline flex items-center justify-between py-0.5"
                      >
                        <span className="truncate">{res.title}</span>
                        <ExternalLink className="w-3 h-3 shrink-0 ml-1 opacity-70" />
                      </a>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {gapData?.partial_skills?.length === 0 && (
              <p className="text-xs text-slate-500 text-center py-6">No partially developed skills.</p>
            )}
          </div>
        </div>

        {/* 3. MISSING CRITICAL SKILLS */}
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/20">
            <div className="flex items-center gap-2">
              <XCircle className="w-4 h-4 text-rose-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-rose-300">
                Missing Skills ({gapData?.missing_skills?.length || 0})
              </span>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">Action Needed</span>
          </div>

          <div className="space-y-3">
            {gapData?.missing_skills?.map((item, idx) => {
              const isHigh = item.importance_level === 'High';
              return (
                <div
                  key={idx}
                  className={`p-4 rounded-2xl glass-panel space-y-3 ${
                    isHigh ? 'border-rose-500/30 ring-1 ring-rose-500/20' : 'border-white/10'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-sm font-bold text-white">{item.skill_name}</span>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                          isHigh ? 'bg-rose-500/20 text-rose-300' : 'bg-slate-700 text-slate-300'
                        }`}
                      >
                        {item.importance_level} Priority
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-[11px] text-slate-400">
                      <Clock className="w-3 h-3 text-cyan-400" />
                      <span>Est. {item.estimated_weeks} weeks • Target: {item.required_proficiency}</span>
                    </div>
                  </div>

                  {item.recommended_resources?.length > 0 && (
                    <div className="pt-2 border-t border-white/5 space-y-1.5">
                      <span className="text-[10px] uppercase tracking-wider font-bold text-slate-400 block">Recommended Resources:</span>
                      {item.recommended_resources.slice(0, 2).map((res, rIdx) => (
                        <a
                          key={rIdx}
                          href={res.url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-xs text-indigo-400 hover:underline flex items-center justify-between py-0.5"
                        >
                          <span className="truncate">{res.title}</span>
                          <ExternalLink className="w-3 h-3 shrink-0 ml-1 opacity-70" />
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
            {gapData?.missing_skills?.length === 0 && (
              <p className="text-xs text-slate-500 text-center py-6">Zero missing skills! You match 100% of this profile.</p>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Action Bridge */}
      <div className="p-6 rounded-3xl glass-panel border border-indigo-500/30 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1 text-center sm:text-left">
          <h4 className="text-base font-bold text-white">Bridge these gaps step-by-step</h4>
          <p className="text-xs text-slate-400">
            SkillBridge AI generates a prioritized, milestone-driven curriculum mapped to your gaps.
          </p>
        </div>

        <NavLink
          to="/roadmap"
          className="px-6 py-3 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2 shrink-0 shadow-lg shadow-indigo-500/25"
        >
          Generate Personalized Roadmap <ArrowRight className="w-4 h-4" />
        </NavLink>
      </div>
    </div>
  );
}
