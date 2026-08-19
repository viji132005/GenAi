import React, { useState, useEffect } from 'react';
import {
  FolderGit2,
  Sparkles,
  Bookmark,
  CheckCircle2,
  Layers,
  Code2,
  ArrowRight,
  RefreshCw,
  ExternalLink,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { projectsAPI } from '../services/api';
import LoadingState from '../components/ui/LoadingState';

const DOMAIN_OPTIONS = ['All', 'AI/ML', 'Data Science', 'Web Development', 'Cybersecurity'];
const DIFFICULTY_OPTIONS = ['All', 'Beginner', 'Intermediate', 'Advanced'];

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);
  const [selectedDomain, setSelectedDomain] = useState('All');
  const [selectedDifficulty, setSelectedDifficulty] = useState('All');
  const [expandedProjects, setExpandedProjects] = useState({});

  const fetchProjects = async (domain = selectedDomain, difficulty = selectedDifficulty) => {
    setLoading(true);
    try {
      const res = await projectsAPI.getProjects(
        domain === 'All' ? null : domain,
        difficulty === 'All' ? null : difficulty
      );
      setProjects(res.data || []);
    } catch (e) {
      console.error('Error fetching projects', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleDomainFilter = (d) => {
    setSelectedDomain(d);
    fetchProjects(d, selectedDifficulty);
  };

  const handleDifficultyFilter = (diff) => {
    setSelectedDifficulty(diff);
    fetchProjects(selectedDomain, diff);
  };

  const handleRegenerate = async () => {
    setRegenerating(true);
    try {
      const res = await projectsAPI.regenerateProjects(
        selectedDomain === 'All' ? null : selectedDomain,
        selectedDifficulty === 'All' ? null : selectedDifficulty
      );
      setProjects(res.data || []);
    } catch (e) {
      console.error('Error regenerating projects', e);
    } finally {
      setRegenerating(false);
    }
  };

  const handleToggleBookmark = async (projectId) => {
    try {
      const res = await projectsAPI.toggleBookmark(projectId);
      setProjects((prev) => prev.map((p) => (p.id === projectId ? res.data : p)));
    } catch (e) {
      console.error('Error bookmarking project', e);
    }
  };

  const toggleExpand = (id) => {
    setExpandedProjects((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold mb-2">
            <FolderGit2 className="w-3.5 h-3.5" />
            <span>AI Architecture & Capstone Blueprints</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            Project Recommendations
          </h1>
          <p className="text-sm text-slate-400">
            Tailored software and machine learning project blueprints designed to bridge your missing skills.
          </p>
        </div>

        <button
          onClick={handleRegenerate}
          disabled={regenerating}
          className="px-4 py-2.5 rounded-xl btn-secondary text-xs font-semibold text-slate-200 hover:text-white flex items-center gap-2 disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-cyan-400 ${regenerating ? 'animate-spin' : ''}`} />
          {regenerating ? 'Designing Projects...' : 'Generate New Blueprints'}
        </button>
      </div>

      {/* Filters Bar */}
      <div className="p-4 rounded-2xl glass-panel flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold text-slate-400 mr-1">Domain:</span>
          {DOMAIN_OPTIONS.map((d) => (
            <button
              key={d}
              onClick={() => handleDomainFilter(d)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                selectedDomain === d
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white/5 text-slate-400 hover:text-white'
              }`}
            >
              {d}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold text-slate-400 mr-1">Difficulty:</span>
          {DIFFICULTY_OPTIONS.map((diff) => (
            <button
              key={diff}
              onClick={() => handleDifficultyFilter(diff)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                selectedDifficulty === diff
                  ? 'bg-cyan-600 text-white'
                  : 'bg-white/5 text-slate-400 hover:text-white'
              }`}
            >
              {diff}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <LoadingState message="Generating Production Project Architectures..." subtext="Designing real-world problem statements, milestone stages, and portfolio bullet formulas" />
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
          {projects.map((proj) => {
            const isExpanded = expandedProjects[proj.id];
            return (
              <div
                key={proj.id}
                className="p-6 rounded-3xl glass-panel glass-panel-hover flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] uppercase tracking-wider font-bold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        {proj.domain}
                      </span>
                      <span className="text-[10px] uppercase tracking-wider font-bold px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                        {proj.difficulty}
                      </span>
                    </div>

                    <button
                      onClick={() => handleToggleBookmark(proj.id)}
                      className={`p-1.5 rounded-lg transition-colors ${
                        proj.is_bookmarked ? 'text-amber-400 bg-amber-400/10' : 'text-slate-500 hover:text-slate-200'
                      }`}
                      title="Bookmark Project"
                    >
                      <Bookmark className="w-4 h-4 fill-current" />
                    </button>
                  </div>

                  <h3 className="text-lg font-bold font-heading text-white">{proj.title}</h3>
                  <p className="text-xs text-slate-300 leading-relaxed">{proj.problem_statement}</p>

                  {/* Why Suitable */}
                  <div className="p-3 rounded-xl bg-indigo-500/5 border border-indigo-500/15 text-xs text-indigo-200">
                    💡 <strong>Career Fit:</strong> {proj.why_suitable}
                  </div>

                  {/* Tech Stack */}
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
                      Tech Stack:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {proj.tech_stack?.map((t, idx) => (
                        <span key={idx} className="px-2 py-0.5 rounded bg-white/5 border border-white/8 text-slate-300 text-[11px] font-medium">
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Expanded Milestone Stages */}
                  {isExpanded && (
                    <div className="space-y-3 pt-3 border-t border-white/8 animate-in fade-in">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                        4-Stage Development Plan:
                      </span>
                      <div className="space-y-2">
                        {proj.development_phases?.map((stage, sIdx) => (
                          <div key={sIdx} className="p-2.5 rounded-xl bg-white/3 border border-white/5 text-xs text-slate-300">
                            <span className="font-bold text-cyan-300 mr-2">{stage.stage}:</span>
                            <span>{stage.objective}</span>
                          </div>
                        ))}
                      </div>

                      <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300">
                        📄 <strong>Portfolio Value:</strong> {proj.portfolio_value}
                      </div>
                    </div>
                  )}
                </div>

                <div className="pt-3 border-t border-white/8 flex items-center justify-between">
                  <button
                    onClick={() => toggleExpand(proj.id)}
                    className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
                  >
                    {isExpanded ? 'Hide Architecture' : 'View Architecture & Phases'}
                    {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>

                  <span className="text-[11px] text-slate-500 font-medium">
                    {proj.skills_learned?.length} skills targeted
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
