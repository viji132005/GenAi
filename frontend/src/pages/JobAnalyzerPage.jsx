import React, { useState } from 'react';
import {
  Briefcase,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  TrendingUp,
  Building,
  Target,
  FileCode
} from 'lucide-react';
import { jobAPI } from '../services/api';
import ProgressRing from '../components/ui/ProgressRing';
import LoadingState from '../components/ui/LoadingState';

const SAMPLE_JD = `Role: Junior AI/ML Engineer
Company: CloudScale AI
Location: Remote / Hybrid

About the Role:
We are seeking an ambitious Junior AI/ML Engineer to build scalable machine learning inference pipelines and train deep learning models.

Responsibilities:
- Build and maintain model serving microservices using Python and FastAPI
- Train and evaluate deep learning architectures in PyTorch or TensorFlow
- Work closely with backend engineers to integrate models into production using Docker and AWS ECS
- Write robust SQL queries for dataset aggregation and feature extraction

Requirements:
- Strong proficiency in Python, NumPy, Pandas, and Scikit-Learn
- Hands-on experience with PyTorch or deep learning frameworks
- Familiarity with Docker containerization and RESTful APIs
- Working knowledge of SQL and relational databases
- B.E./B.Tech in Computer Science or relevant engineering discipline`;

export default function JobAnalyzerPage() {
  const [jobTitle, setJobTitle] = useState('Junior AI/ML Engineer');
  const [company, setCompany] = useState('CloudScale AI');
  const [jobDescription, setJobDescription] = useState(SAMPLE_JD);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!jobDescription.trim()) return;

    setLoading(true);
    try {
      const res = await jobAPI.analyzeJob({
        job_title: jobTitle,
        company: company,
        job_description: jobDescription
      });
      setResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to analyze job description.');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadSample = () => {
    setJobTitle('Junior AI/ML Engineer');
    setCompany('CloudScale AI');
    setJobDescription(SAMPLE_JD);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-semibold mb-2">
          <Briefcase className="w-3.5 h-3.5" />
          <span>AI Job Compatibility & Requirement Parser</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
          Job Description Analyzer
        </h1>
        <p className="text-sm text-slate-400">
          Paste any live job posting to compare extracted requirements directly against your verified student profile.
        </p>
      </div>

      {/* Input Card */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 shadow-2xl">
        <form onSubmit={handleAnalyze} className="space-y-5">
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Job Title</label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Machine Learning Engineer"
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Company Name (Optional)</label>
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="e.g. Google / Microsoft / Startup"
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-semibold text-slate-300">Job Description Text</label>
              <button
                type="button"
                onClick={handleLoadSample}
                className="text-xs text-indigo-400 hover:underline font-medium"
              >
                Load Sample AI/ML Job Posting
              </button>
            </div>
            <textarea
              rows={8}
              required
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste responsibilities, requirements, and tech stack from LinkedIn or job board..."
              className="w-full p-4 rounded-2xl bg-white/5 border border-white/10 text-white text-xs font-mono focus:outline-none focus:border-indigo-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading || !jobDescription.trim()}
            className="px-8 py-3 rounded-xl btn-primary text-sm font-bold text-white flex items-center gap-2 disabled:opacity-50"
          >
            {loading ? 'Evaluating Match Compatibility...' : 'Analyze Job Fit with AI'}
            <Sparkles className="w-4 h-4" />
          </button>
        </form>
      </div>

      {loading && (
        <LoadingState message="Extracting Job Requirements..." subtext="Comparing required frameworks, years of experience, and responsibilities with your profile" />
      )}

      {/* Analysis Output */}
      {result && !loading && (
        <div className="space-y-6">
          {/* Main Score Banner */}
          <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-indigo-500/30 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
            <div className="space-y-2 text-center md:text-left">
              <div className="flex items-center justify-center md:justify-start gap-2">
                <Building className="w-4 h-4 text-slate-400" />
                <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider">
                  {result.company || 'Tech Company'}
                </span>
              </div>
              <h2 className="text-2xl font-bold font-heading text-white">{result.job_title}</h2>
              <p className="text-xs text-slate-400">
                Experience Requirement: <span className="text-slate-200 font-semibold">{result.experience_requirements}</span>
              </p>
            </div>

            <div className="flex items-center gap-4">
              <ProgressRing
                percentage={result.match_score}
                size={80}
                strokeWidth={7}
                color={result.match_score >= 75 ? '#10B981' : result.match_score >= 50 ? '#6366F1' : '#F59E0B'}
                label="Job Match"
              />
            </div>
          </div>

          {/* Matches vs Gaps */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Strong Matches */}
            <div className="p-6 rounded-3xl glass-panel space-y-4">
              <div className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-5 h-5" />
                <h3 className="text-base font-bold font-heading text-white">
                  Strong Matches ({result.strong_matches?.length || 0})
                </h3>
              </div>
              <p className="text-xs text-slate-400">Skills you have that directly satisfy this job posting:</p>
              <div className="flex flex-wrap gap-2">
                {result.strong_matches?.map((s, i) => (
                  <span key={i} className="px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" /> {s}
                  </span>
                ))}
              </div>
            </div>

            {/* Critical Skill Gaps */}
            <div className="p-6 rounded-3xl glass-panel space-y-4">
              <div className="flex items-center gap-2 text-rose-400">
                <AlertCircle className="w-5 h-5" />
                <h3 className="text-base font-bold font-heading text-white">
                  Missing Requirements ({result.skill_gaps?.length || 0})
                </h3>
              </div>
              <p className="text-xs text-slate-400">Prerequisites you must bridge before applying:</p>
              <div className="flex flex-wrap gap-2">
                {result.skill_gaps?.map((s, i) => (
                  <span key={i} className="px-3 py-1.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-1.5">
                    <AlertCircle className="w-3.5 h-3.5" /> {s}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Action Plan */}
          {result.action_plan?.length > 0 && (
            <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-indigo-500/30 space-y-4">
              <h3 className="text-base font-bold font-heading text-white flex items-center gap-2">
                <Target className="w-5 h-5 text-indigo-400" />
                <span>3-Step Immediate Action Plan to Become Competitive</span>
              </h3>
              <div className="space-y-3">
                {result.action_plan.map((step, idx) => (
                  <div key={idx} className="p-4 rounded-2xl bg-white/4 border border-white/8 text-xs text-slate-200 flex items-start gap-3">
                    <span className="w-6 h-6 rounded-lg bg-indigo-500/20 text-indigo-400 font-bold flex items-center justify-center shrink-0">
                      {idx + 1}
                    </span>
                    <span className="leading-relaxed mt-0.5">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
