import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  Sparkles,
  Target,
  ArrowRight,
  TrendingUp,
  Award,
  GitPullRequest,
  Map,
  FileText,
  Mic,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  ChevronRight,
  Zap
} from 'lucide-react';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';
import { analyticsAPI } from '../services/api';
import ProgressRing from '../components/ui/ProgressRing';
import LoadingState from '../components/ui/LoadingState';

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await analyticsAPI.getDashboard();
        setData(res.data);
      } catch (e) {
        console.error('Error fetching dashboard', e);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return <LoadingState message="Synthesizing career dashboard..." subtext="Aggregating skill mastery, roadmap velocity, and interview scores" />;
  }

  const radarData = data?.radar_metrics ? Object.entries(data.radar_metrics).map(([key, val]) => ({
    subject: key,
    value: val,
    fullMark: 100
  })) : [];

  const timelineData = data?.timeline_metrics || [];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Welcome Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white flex items-center gap-3">
            Welcome, {data?.user_name || 'Student'}! 👋
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Targeting <span className="text-indigo-400 font-bold">{data?.target_career}</span> • Semester 6 Engineering
          </p>
        </div>

        <div className="flex items-center gap-3">
          <NavLink
            to="/roadmap"
            className="px-4 py-2 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2 shadow-sm"
          >
            <Map className="w-3.5 h-3.5" /> Continue Roadmap
          </NavLink>
        </div>
      </div>

      {/* Hero "Recommended Next Action" Card */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-indigo-900/40 via-slate-900/60 to-cyan-950/40 border border-indigo-500/30 shadow-xl relative overflow-hidden">
        <div className="absolute -top-12 -right-12 w-44 h-44 bg-indigo-500/10 rounded-full blur-2xl pointer-events-none" />
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-[11px] font-bold">
              <Zap className="w-3 h-3 text-indigo-400" />
              <span>AI RECOMMENDED NEXT ACTION</span>
            </div>
            <h3 className="text-lg font-bold font-heading text-white">
              {data?.recommended_next_action || "Complete your next priority skill milestone."}
            </h3>
            <p className="text-xs text-slate-400">
              Directly aligned with your active {data?.target_career} roadmap and highest impact gap.
            </p>
          </div>
          <NavLink
            to="/skill-gap"
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center gap-2 transition-all shrink-0 shadow-lg shadow-indigo-600/30"
          >
            Take Action <ArrowRight className="w-4 h-4" />
          </NavLink>
        </div>
      </div>

      {/* 6 Key KPI Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        {[
          { label: 'Career Match', value: data?.career_match_percentage || 82, suffix: '%', color: '#6366F1', sub: 'Against Target' },
          { label: 'Career Readiness', value: data?.career_readiness_score || 68, suffix: '%', color: '#06B6D4', sub: 'Industry Metric' },
          { label: 'Resume Score', value: data?.resume_score || 74, suffix: '/100', color: '#10B981', sub: 'ATS Evaluated' },
          { label: 'Skill Mastery', value: data?.skill_completion_percentage || 78, suffix: '%', color: '#8B5CF6', sub: 'Verified Skills' },
          { label: 'Interview Score', value: data?.interview_readiness_score || 61, suffix: '%', color: '#F59E0B', sub: 'Mock Prepared' },
          { label: 'Roadmap Velocity', value: data?.roadmap_progress_percentage || 43, suffix: '%', color: '#EC4899', sub: 'Tasks Completed' },
        ].map((kpi, idx) => (
          <div key={idx} className="p-4 rounded-2xl glass-panel glass-panel-hover flex flex-col items-center justify-between text-center">
            <ProgressRing
              percentage={kpi.value}
              size={64}
              strokeWidth={5}
              color={kpi.color}
            />
            <div className="mt-2">
              <span className="text-xs font-bold text-slate-200 block">{kpi.label}</span>
              <span className="text-[10px] text-slate-400">{kpi.sub}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Analytics & Charts Section */}
      <div className="grid lg:grid-cols-12 gap-6">
        {/* Radar Competency Chart */}
        <div className="lg:col-span-5 p-6 rounded-3xl glass-panel flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold font-heading text-white">Competency Radar</h3>
              <p className="text-xs text-slate-400">Multi-dimensional engineering readiness</p>
            </div>
            <Sparkles className="w-4 h-4 text-indigo-400" />
          </div>

          <div className="w-full h-64 flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.08)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94A3B8', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="rgba(255,255,255,0.1)" />
                <Radar
                  name="Rahul"
                  dataKey="value"
                  stroke="#6366F1"
                  fill="#6366F1"
                  fillOpacity={0.4}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Readiness Trajectory Line Chart */}
        <div className="lg:col-span-7 p-6 rounded-3xl glass-panel flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold font-heading text-white">Career Readiness Trajectory</h3>
              <p className="text-xs text-slate-400">Measurable monthly improvement timeline</p>
            </div>
            <TrendingUp className="w-4 h-4 text-cyan-400" />
          </div>

          <div className="w-full h-64 flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="month" stroke="#64748B" fontSize={11} />
                <YAxis domain={[0, 100]} stroke="#64748B" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', fontSize: '12px' }}
                />
                <Line type="monotone" dataKey="readiness" name="Career Readiness" stroke="#6366F1" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="skill_completion" name="Skills" stroke="#06B6D4" strokeWidth={2} strokeDasharray="4 4" />
                <Line type="monotone" dataKey="resume_score" name="Resume" stroke="#10B981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Bottom Grid: Top Missing Skills & Recent Insights */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Top Missing Skills */}
        <div className="p-6 rounded-3xl glass-panel">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <GitPullRequest className="w-4 h-4 text-indigo-400" />
              <h3 className="text-base font-bold font-heading text-white">Top Missing Skills</h3>
            </div>
            <NavLink to="/skill-gap" className="text-xs font-semibold text-indigo-400 hover:underline flex items-center gap-1">
              View Matrix <ChevronRight className="w-3 h-3" />
            </NavLink>
          </div>

          <p className="text-xs text-slate-400 mb-4">
            Acquiring these 3 skills will boost your career match to over 90%.
          </p>

          <div className="space-y-3">
            {data?.top_missing_skills?.map((sk, i) => (
              <div key={i} className="p-3.5 rounded-2xl bg-white/4 border border-white/8 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-400 font-bold text-xs flex items-center justify-center border border-rose-500/20">
                    !
                  </div>
                  <div>
                    <span className="text-sm font-bold text-white">{sk}</span>
                    <span className="text-[11px] text-slate-400 block">High Priority Gap for {data?.target_career}</span>
                  </div>
                </div>
                <NavLink
                  to="/skill-gap"
                  className="px-3 py-1 rounded-lg bg-indigo-500/20 text-indigo-300 text-xs font-semibold hover:bg-indigo-500/30 transition-colors"
                >
                  Learn
                </NavLink>
              </div>
            ))}
          </div>
        </div>

        {/* Recent AI Insights */}
        <div className="p-6 rounded-3xl glass-panel">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <h3 className="text-base font-bold font-heading text-white">Recent AI Insights</h3>
            </div>
            <NavLink to="/assistant" className="text-xs font-semibold text-cyan-400 hover:underline flex items-center gap-1">
              Ask AI Co-Pilot <ChevronRight className="w-3 h-3" />
            </NavLink>
          </div>

          <div className="space-y-3">
            {data?.recent_insights?.map((ins, i) => (
              <NavLink
                key={i}
                to={ins.action_url}
                className="p-3.5 rounded-2xl bg-white/4 border border-white/8 block hover:border-indigo-500/30 transition-all group"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-indigo-300">{ins.title}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-white/5 text-slate-400">{ins.category}</span>
                </div>
                <p className="text-xs text-slate-400 group-hover:text-slate-200 transition-colors">
                  {ins.description}
                </p>
              </NavLink>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
