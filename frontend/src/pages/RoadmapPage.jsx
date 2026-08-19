import React, { useState, useEffect } from 'react';
import {
  Map,
  Sparkles,
  CheckCircle2,
  Circle,
  ExternalLink,
  Clock,
  Code2,
  Layers,
  Award,
  RefreshCw,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { roadmapAPI } from '../services/api';
import LoadingState from '../components/ui/LoadingState';

export default function RoadmapPage() {
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);
  const [expandedPhases, setExpandedPhases] = useState({});

  const fetchRoadmap = async () => {
    setLoading(true);
    try {
      const res = await roadmapAPI.getRoadmap();
      setRoadmap(res.data);
      // Auto-expand all phases initially
      const exp = {};
      res.data.tasks?.forEach((t) => { exp[t.phase_number] = true; });
      setExpandedPhases(exp);
    } catch (e) {
      console.error('Error fetching roadmap', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, []);

  const handleToggleTask = async (taskId, currentStatus) => {
    try {
      const res = await roadmapAPI.toggleTask(taskId, !currentStatus);
      setRoadmap(res.data);
    } catch (e) {
      console.error('Error toggling task', e);
    }
  };

  const handleRegenerate = async () => {
    setRegenerating(true);
    try {
      const res = await roadmapAPI.regenerateRoadmap();
      setRoadmap(res.data);
      const exp = {};
      res.data.tasks?.forEach((t) => { exp[t.phase_number] = true; });
      setExpandedPhases(exp);
    } catch (e) {
      console.error('Error regenerating roadmap', e);
    } finally {
      setRegenerating(false);
    }
  };

  const togglePhaseExpand = (phaseNum) => {
    setExpandedPhases((prev) => ({ ...prev, [phaseNum]: !prev[phaseNum] }));
  };

  if (loading) {
    return <LoadingState message="Curating personalized curriculum..." subtext="Structuring milestone phases, project checkpoints, and resource sequences" />;
  }

  // Group tasks by phase
  const phases = {};
  roadmap?.tasks?.forEach((task) => {
    if (!phases[task.phase_number]) {
      phases[task.phase_number] = {
        name: task.phase_name,
        tasks: []
      };
    }
    phases[task.phase_number].tasks.push(task);
  });

  const totalTasks = roadmap?.tasks?.length || 0;
  const completedTasks = roadmap?.tasks?.filter((t) => t.is_completed).length || 0;

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-2">
            <Map className="w-3.5 h-3.5" />
            <span>AI Structured Curriculum</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            {roadmap?.title || 'Personalized Career Roadmap'}
          </h1>
          <p className="text-sm text-slate-400">
            Targeting <span className="text-indigo-400 font-bold">{roadmap?.career_title}</span> • Estimated {roadmap?.target_duration_months || 6} Months
          </p>
        </div>

        <button
          onClick={handleRegenerate}
          disabled={regenerating}
          className="px-4 py-2.5 rounded-xl btn-secondary text-xs font-semibold text-slate-200 hover:text-white flex items-center gap-2 disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-indigo-400 ${regenerating ? 'animate-spin' : ''}`} />
          {regenerating ? 'Re-synthesizing...' : 'Regenerate with AI'}
        </button>
      </div>

      {/* Progress & Overview Card */}
      <div className="p-6 rounded-3xl glass-panel border border-indigo-500/20 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">Curriculum Velocity</span>
            <p className="text-sm text-slate-300 font-medium">{roadmap?.overview_summary}</p>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <span className="text-2xl font-extrabold text-white font-heading">
              {roadmap?.completion_percentage}%
            </span>
            <span className="text-xs text-slate-400 font-medium">
              ({completedTasks} of {totalTasks} tasks done)
            </span>
          </div>
        </div>

        {/* Linear Progress Bar */}
        <div className="w-full h-3 rounded-full bg-white/10 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 via-cyan-400 to-emerald-400 transition-all duration-500 rounded-full"
            style={{ width: `${roadmap?.completion_percentage || 0}%` }}
          />
        </div>
      </div>

      {/* Phased Roadmap Timeline Tree */}
      <div className="space-y-6">
        {Object.entries(phases).map(([phaseNum, phaseData]) => {
          const isExpanded = expandedPhases[phaseNum] !== false;
          const phaseTasksCompleted = phaseData.tasks.filter((t) => t.is_completed).length;
          const phaseTotal = phaseData.tasks.length;
          const isPhaseDone = phaseTasksCompleted === phaseTotal;

          return (
            <div key={phaseNum} className="glass-panel rounded-3xl border border-white/8 overflow-hidden">
              {/* Phase Header Accordion */}
              <button
                type="button"
                onClick={() => togglePhaseExpand(phaseNum)}
                className="w-full p-5 sm:p-6 flex items-center justify-between bg-white/2 hover:bg-white/4 transition-colors text-left"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xs ${
                      isPhaseDone
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                    }`}
                  >
                    {isPhaseDone ? <CheckCircle2 className="w-5 h-5" /> : `P${phaseNum}`}
                  </div>
                  <div>
                    <h3 className="text-base font-bold font-heading text-white">{phaseData.name}</h3>
                    <p className="text-xs text-slate-400">
                      {phaseTasksCompleted} of {phaseTotal} milestones completed
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {isPhaseDone && (
                    <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                      Phase Mastered
                    </span>
                  )}
                  {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                </div>
              </button>

              {/* Tasks List */}
              {isExpanded && (
                <div className="p-5 sm:p-6 border-t border-white/5 space-y-4">
                  {phaseData.tasks.map((task) => (
                    <div
                      key={task.id}
                      className={`p-5 rounded-2xl transition-all border ${
                        task.is_completed
                          ? 'bg-emerald-500/5 border-emerald-500/20'
                          : 'bg-white/3 border-white/5 hover:border-white/15'
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        {/* Checkbox */}
                        <button
                          type="button"
                          onClick={() => handleToggleTask(task.id, task.is_completed)}
                          className="mt-0.5 text-slate-400 hover:text-emerald-400 transition-colors shrink-0"
                        >
                          {task.is_completed ? (
                            <CheckCircle2 className="w-6 h-6 text-emerald-400" />
                          ) : (
                            <Circle className="w-6 h-6 text-slate-500" />
                          )}
                        </button>

                        <div className="flex-1 space-y-2.5">
                          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                            <h4
                              className={`text-sm font-bold ${
                                task.is_completed ? 'text-slate-300 line-through' : 'text-white'
                              }`}
                            >
                              {task.task_title}
                            </h4>
                            <div className="flex items-center gap-2 text-xs text-slate-400">
                              <Clock className="w-3.5 h-3.5 text-cyan-400" />
                              <span>{task.estimated_hours} Hours</span>
                            </div>
                          </div>

                          <p className="text-xs text-slate-300 leading-relaxed">
                            {task.description}
                          </p>

                          {/* Skills badges */}
                          {task.skills_covered?.length > 0 && (
                            <div className="flex flex-wrap gap-1.5 pt-1">
                              {task.skills_covered.map((s, idx) => (
                                <span
                                  key={idx}
                                  className="px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-[10px] font-semibold"
                                >
                                  {s}
                                </span>
                              ))}
                            </div>
                          )}

                          {/* Project Checkpoint */}
                          {task.project_checkpoint && (
                            <div className="p-3 rounded-xl bg-white/2 border border-white/5 flex items-start gap-2.5 text-xs text-slate-300">
                              <Code2 className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                              <div>
                                <span className="font-bold text-cyan-300 block mb-0.5">Practical Checkpoint:</span>
                                <span>{task.project_checkpoint}</span>
                              </div>
                            </div>
                          )}

                          {/* Resource Links */}
                          {task.learning_resources?.length > 0 && (
                            <div className="pt-2 flex flex-wrap gap-3">
                              {task.learning_resources.map((res, rIdx) => (
                                <a
                                  key={rIdx}
                                  href={res.url}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="text-xs text-indigo-400 hover:underline inline-flex items-center gap-1 font-medium"
                                >
                                  <ExternalLink className="w-3 h-3 opacity-70" />
                                  <span>{res.title}</span>
                                </a>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
