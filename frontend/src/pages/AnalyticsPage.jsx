import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  TrendingUp,
  Award,
  CheckCircle2,
  Calendar,
  Layers,
  Sparkles,
  Zap,
  Target
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { analyticsAPI } from '../services/api';
import ProgressRing from '../components/ui/ProgressRing';
import LoadingState from '../components/ui/LoadingState';

export default function AnalyticsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await analyticsAPI.getDashboard();
        setData(res.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) {
    return <LoadingState message="Aggregating Progress Analytics..." subtext="Compiling historical velocity curves, resume score progression, and interview metrics" />;
  }

  const timelineData = data?.timeline_metrics || [];
  const radarData = data?.radar_metrics ? Object.entries(data.radar_metrics).map(([key, val]) => ({
    subject: key,
    value: val,
    fullMark: 100
  })) : [];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-2">
          <BarChart3 className="w-3.5 h-3.5" />
          <span>Continuous Progress Telemetry</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
          Progress & Career Readiness Analytics
        </h1>
        <p className="text-sm text-slate-400">
          Track your measurable engineering readiness and milestone velocity over time.
        </p>
      </div>

      {/* Highlights Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Overall Readiness', value: `${data?.career_readiness_score || 68}%`, sub: '+29% from Month 1', color: 'text-indigo-400' },
          { label: 'Curriculum Velocity', value: `${data?.roadmap_progress_percentage || 43}%`, sub: 'Active Phase 3 of 6', color: 'text-cyan-400' },
          { label: 'ATS Score Growth', value: `${data?.resume_score || 74}/100`, sub: '+16 pts improvement', color: 'text-emerald-400' },
          { label: 'Mock Interview Readiness', value: `${data?.interview_readiness_score || 61}%`, sub: '3 rounds completed', color: 'text-amber-400' },
        ].map((item, idx) => (
          <div key={idx} className="p-5 rounded-2xl glass-panel flex flex-col justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">{item.label}</span>
            <div className="my-2">
              <span className={`text-2xl font-extrabold font-heading ${item.color}`}>{item.value}</span>
            </div>
            <span className="text-[11px] text-slate-400 font-medium">{item.sub}</span>
          </div>
        ))}
      </div>

      {/* Main Readiness Trajectory Chart */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="text-lg font-bold font-heading text-white">4-Month Readiness Growth Trajectory</h3>
            <p className="text-xs text-slate-400">Demonstrates consistent, measurable improvement across all assessment pillars</p>
          </div>
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            Target: 85% by Graduation
          </span>
        </div>

        <div className="w-full h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={timelineData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="month" stroke="#64748B" fontSize={12} />
              <YAxis domain={[0, 100]} stroke="#64748B" fontSize={12} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0F172A', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', fontSize: '12px' }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Line type="monotone" dataKey="readiness" name="Career Readiness (%)" stroke="#6366F1" strokeWidth={3} dot={{ r: 5 }} />
              <Line type="monotone" dataKey="skill_completion" name="Skill Mastery (%)" stroke="#06B6D4" strokeWidth={2} />
              <Line type="monotone" dataKey="resume_score" name="Resume ATS Score" stroke="#10B981" strokeWidth={2} />
              <Line type="monotone" dataKey="interview_score" name="Interview Readiness" stroke="#F59E0B" strokeWidth={2} strokeDasharray="3 3" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Competency Radar & Multi-Category Breakdown */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="p-6 rounded-3xl glass-panel flex flex-col">
          <h3 className="text-base font-bold font-heading text-white mb-2">Multi-Disciplinary Radar</h3>
          <p className="text-xs text-slate-400 mb-4">Competency distribution for {data?.target_career}</p>
          <div className="w-full h-72 flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.08)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94A3B8', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="rgba(255,255,255,0.1)" />
                <Radar name="Student" dataKey="value" stroke="#06B6D4" fill="#06B6D4" fillOpacity={0.35} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Milestone Achievement Log */}
        <div className="p-6 rounded-3xl glass-panel space-y-4">
          <h3 className="text-base font-bold font-heading text-white">Milestone History</h3>
          <p className="text-xs text-slate-400">Key achievements validated in the system</p>
          <div className="space-y-3">
            {[
              { date: 'Month 1', title: 'Python & Linear Algebra Certified', desc: 'Completed Phase 1 foundational milestone modules with 100% score.' },
              { date: 'Month 2', title: 'Scikit-Learn ML Churn Model Built', desc: 'Engineered XGBoost classification pipeline achieving 88% ROC-AUC.' },
              { date: 'Month 3', title: 'Resume ATS Audit Completed', desc: 'Optimized project descriptions into Google XYZ quantifiable format.' },
              { date: 'Month 4', title: 'Technical Mock Interview Cleared', desc: 'Scored 76% on intermediate AI/ML Engineering problem solving.' },
            ].map((m, idx) => (
              <div key={idx} className="p-3.5 rounded-2xl bg-white/3 border border-white/5 flex items-start gap-3">
                <div className="w-8 h-8 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-xs shrink-0">
                  ✓
                </div>
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-white">{m.title}</span>
                    <span className="text-[10px] text-slate-500">{m.date}</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5 leading-snug">{m.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
