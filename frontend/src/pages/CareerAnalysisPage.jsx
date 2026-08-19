import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  Compass,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  TrendingUp,
  DollarSign,
  Briefcase,
  Layers,
  FolderGit2,
  Target
} from 'lucide-react';
import { careerAPI } from '../services/api';
import ProgressRing from '../components/ui/ProgressRing';
import LoadingState from '../components/ui/LoadingState';

export default function CareerAnalysisPage() {
  const [analysis, setAnalysis] = useState(null);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updatingGoal, setUpdatingGoal] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const fetchCareerAnalysis = async () => {
    setLoading(true);
    try {
      const res = await careerAPI.analyzeCareer();
      setAnalysis(res.data);
      if (res.data.top_recommendations?.length > 0) {
        setSelectedCareer(res.data.top_recommendations[0]);
      }
    } catch (e) {
      console.error('Error fetching career analysis', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCareerAnalysis();
  }, []);

  const handleSetTarget = async (careerTitle) => {
    setUpdatingGoal(true);
    try {
      await careerAPI.setTargetCareer(careerTitle);
      setSuccessMsg(`Target career goal successfully updated to ${careerTitle}!`);
      setTimeout(() => setSuccessMsg(''), 3500);
      await fetchCareerAnalysis();
    } catch (e) {
      console.error('Failed to set target career', e);
    } finally {
      setUpdatingGoal(false);
    }
  };

  if (loading) {
    return <LoadingState message="AI Career Recommendation Engine is running..." subtext="Evaluating your academic courses, skill proficiencies, and project experiences against industry taxonomies" />;
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-2">
            <Compass className="w-3.5 h-3.5" />
            <span>AI Career Match & Compatibility Engine</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            Career Recommendations
          </h1>
          <p className="text-sm text-slate-400">
            Personalized compatibility scores based on your real skills and academic factors.
          </p>
        </div>

        <button
          onClick={fetchCareerAnalysis}
          className="px-4 py-2 rounded-xl btn-secondary text-xs font-semibold text-slate-200 hover:text-white flex items-center gap-2"
        >
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" /> Re-analyze Profile
        </button>
      </div>

      {successMsg && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-sm flex items-center gap-3">
          <CheckCircle2 className="w-5 h-5 shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {/* Top Profile Summary Banner */}
      <div className="p-6 rounded-3xl glass-panel border border-indigo-500/20 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-2xl">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">AI Profile Assessment</span>
          <p className="text-sm text-slate-200 leading-relaxed font-medium">
            {analysis?.overall_profile_summary}
          </p>
          <p className="text-xs text-slate-400">
            Current Target Career: <span className="text-white font-bold">{analysis?.target_career}</span>
          </p>
        </div>
        <div className="flex items-center gap-6 border-t md:border-t-0 md:border-l border-white/10 pt-4 md:pt-0 md:pl-6">
          <ProgressRing percentage={analysis?.readiness_score || 68} size={76} strokeWidth={6} color="#06B6D4" label="Readiness" />
        </div>
      </div>

      {/* Recommendations Cards Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {analysis?.top_recommendations?.map((item, idx) => {
          const isSelected = selectedCareer?.career_title === item.career_title;
          const isTarget = analysis?.target_career?.toLowerCase() === item.career_title?.toLowerCase();

          return (
            <div
              key={idx}
              onClick={() => setSelectedCareer(item)}
              className={`p-6 rounded-3xl glass-panel cursor-pointer transition-all flex flex-col justify-between ${
                isSelected
                  ? 'border-indigo-500 ring-2 ring-indigo-500/30 bg-indigo-950/20'
                  : 'hover:border-white/20'
              }`}
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-4">
                  <div>
                    <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-white/5 text-slate-400 font-bold block w-fit mb-1.5">
                      {item.category || 'Engineering'}
                    </span>
                    <h3 className="text-lg font-bold font-heading text-white">{item.career_title}</h3>
                  </div>
                  <ProgressRing percentage={item.match_percentage} size={54} strokeWidth={5} color={item.match_percentage >= 75 ? '#10B981' : item.match_percentage >= 60 ? '#6366F1' : '#F59E0B'} />
                </div>

                <p className="text-xs text-slate-300 line-clamp-3 mb-4 leading-relaxed">
                  {item.why_matches}
                </p>
              </div>

              <div className="pt-4 border-t border-white/8 flex items-center justify-between">
                <span className="text-xs font-semibold text-emerald-400">{item.average_salary}</span>
                {isTarget ? (
                  <span className="text-[11px] font-bold text-indigo-400 px-2.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 flex items-center gap-1">
                    <Target className="w-3 h-3" /> Active Goal
                  </span>
                ) : (
                  <span className="text-xs font-medium text-slate-400 hover:text-white flex items-center gap-1">
                    Details <ArrowRight className="w-3 h-3" />
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Career Detailed Drilldown Panel */}
      {selectedCareer && (
        <div className="p-8 rounded-3xl glass-panel border border-indigo-500/30 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
            <div>
              <div className="flex items-center gap-3 mb-1">
                <h2 className="text-2xl font-bold font-heading text-white">{selectedCareer.career_title}</h2>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-semibold border border-indigo-500/30">
                  {selectedCareer.match_percentage}% Match
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Industry Outlook: <span className="text-emerald-400 font-semibold">{selectedCareer.growth_outlook}</span> • Average Compensation: <span className="text-white font-semibold">{selectedCareer.average_salary}</span>
              </p>
            </div>

            {analysis?.target_career?.toLowerCase() !== selectedCareer.career_title?.toLowerCase() && (
              <button
                disabled={updatingGoal}
                onClick={() => handleSetTarget(selectedCareer.career_title)}
                className="px-6 py-2.5 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2 shrink-0 disabled:opacity-50"
              >
                <Target className="w-4 h-4" />
                {updatingGoal ? 'Updating Goal...' : 'Set as My Target Career'}
              </button>
            )}
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Why it matches & strengths */}
            <div className="space-y-4">
              <div>
                <h4 className="text-xs uppercase font-bold tracking-wider text-indigo-400 mb-2">Why This Career Matches</h4>
                <p className="text-sm text-slate-300 leading-relaxed bg-white/3 p-4 rounded-2xl border border-white/5">
                  {selectedCareer.why_matches}
                </p>
              </div>

              <div>
                <h4 className="text-xs uppercase font-bold tracking-wider text-emerald-400 mb-2">Existing Strengths</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedCareer.existing_strengths?.map((s, i) => (
                    <span key={i} className="px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5" /> {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Missing Skills & Tech */}
            <div className="space-y-4">
              <div>
                <h4 className="text-xs uppercase font-bold tracking-wider text-rose-400 mb-2">Missing Skills to Master</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedCareer.missing_skills?.map((s, i) => (
                    <span key={i} className="px-3 py-1.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-1.5">
                      <AlertCircle className="w-3.5 h-3.5" /> {s}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="text-xs uppercase font-bold tracking-wider text-cyan-400 mb-2">Suggested Core Technologies</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedCareer.suggested_technologies?.map((tech, i) => (
                    <span key={i} className="px-2.5 py-1 rounded-lg bg-white/5 border border-white/8 text-slate-300 text-xs font-medium">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Typical Responsibilities */}
          <div>
            <h4 className="text-xs uppercase font-bold tracking-wider text-slate-400 mb-2">Typical Industry Responsibilities</h4>
            <div className="grid sm:grid-cols-2 gap-2.5">
              {selectedCareer.typical_responsibilities?.map((resp, i) => (
                <div key={i} className="p-3 rounded-xl bg-white/3 border border-white/5 flex items-start gap-2.5 text-xs text-slate-300">
                  <Briefcase className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                  <span>{resp}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Suggested Capstone Projects & Learning Path */}
          <div className="p-5 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <span className="text-[11px] font-bold text-indigo-300 uppercase tracking-wider">Recommended Learning Path</span>
              <p className="text-xs text-slate-200">{selectedCareer.learning_path_summary}</p>
            </div>
            <NavLink
              to="/skill-gap"
              className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shrink-0 transition-colors"
            >
              Analyze Skill Gaps
            </NavLink>
          </div>
        </div>
      )}
    </div>
  );
}
