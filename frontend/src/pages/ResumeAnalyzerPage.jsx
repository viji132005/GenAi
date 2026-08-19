import React, { useState, useEffect } from 'react';
import {
  FileText,
  UploadCloud,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  TrendingUp,
  FileCode,
  Layers,
  Award,
  RefreshCw,
  Copy,
  Check
} from 'lucide-react';
import { resumeAPI } from '../services/api';
import ProgressRing from '../components/ui/ProgressRing';
import LoadingState from '../components/ui/LoadingState';

export default function ResumeAnalyzerPage() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' or 'paste'
  const [pastedText, setPastedText] = useState('');
  const [copiedIdx, setCopiedIdx] = useState(null);

  const fetchLatestAnalysis = async () => {
    setLoading(true);
    try {
      const res = await resumeAPI.getLatest();
      setAnalysis(res.data);
    } catch (e) {
      console.log('No existing resume found', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLatestAnalysis();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await resumeAPI.uploadResume(formData);
      setAnalysis(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to analyze resume PDF.');
    } finally {
      setUploading(false);
    }
  };

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!pastedText.trim()) return;

    setUploading(true);
    try {
      const res = await resumeAPI.analyzeText(pastedText, 'Pasted_Resume.txt');
      setAnalysis(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to analyze resume text.');
    } finally {
      setUploading(false);
    }
  };

  const handleCopyBullet = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold mb-2">
          <FileText className="w-3.5 h-3.5" />
          <span>AI Resume & ATS Optimization Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
          Resume Analyzer
        </h1>
        <p className="text-sm text-slate-400">
          Audit your technical resume against Applicant Tracking Systems and modern engineering hiring standards.
        </p>
      </div>

      {/* Upload & Input Section */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 shadow-2xl">
        <div className="flex items-center gap-4 border-b border-white/8 pb-4 mb-6">
          <button
            onClick={() => setActiveTab('upload')}
            className={`text-xs font-bold px-4 py-2 rounded-xl transition-all ${
              activeTab === 'upload' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Upload PDF / Document
          </button>
          <button
            onClick={() => setActiveTab('paste')}
            className={`text-xs font-bold px-4 py-2 rounded-xl transition-all ${
              activeTab === 'paste' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Paste Plain Text
          </button>
        </div>

        {activeTab === 'upload' ? (
          <div className="border-2 border-dashed border-white/15 hover:border-indigo-500/50 rounded-2xl p-8 sm:p-12 text-center transition-all bg-white/2">
            <input
              type="file"
              id="resume-upload"
              accept=".pdf,.txt"
              onChange={handleFileUpload}
              className="hidden"
              disabled={uploading}
            />
            <label htmlFor="resume-upload" className="cursor-pointer flex flex-col items-center">
              <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-4">
                <UploadCloud className="w-8 h-8" />
              </div>
              <h3 className="text-base font-bold text-white mb-1">
                {uploading ? 'Analyzing PDF with AI...' : 'Click or Drag & Drop your Resume PDF'}
              </h3>
              <p className="text-xs text-slate-400 max-w-sm">
                Supports PDF and TXT formats up to 5MB. PyPDF extraction with secure ATS parsing.
              </p>
            </label>
          </div>
        ) : (
          <form onSubmit={handleTextSubmit} className="space-y-4">
            <textarea
              rows={8}
              value={pastedText}
              onChange={(e) => setPastedText(e.target.value)}
              placeholder="Paste your raw resume text, education, projects, and work experience here..."
              className="w-full p-4 rounded-2xl bg-white/5 border border-white/10 text-white text-xs font-mono focus:outline-none focus:border-indigo-500"
            />
            <button
              type="submit"
              disabled={uploading || !pastedText.trim()}
              className="px-6 py-2.5 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2 disabled:opacity-50"
            >
              {uploading ? 'Analyzing...' : 'Run ATS Audit on Text'}
              <Sparkles className="w-4 h-4" />
            </button>
          </form>
        )}
      </div>

      {uploading && (
        <LoadingState message="Deep ATS Audit in progress..." subtext="Extracting project metrics, evaluating keyword relevance, and generating XYZ bullet rewrites" />
      )}

      {/* Analysis Results */}
      {analysis && !uploading && (
        <div className="space-y-8">
          {/* Scorecards Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { label: 'Overall Score', score: analysis.overall_score, color: '#6366F1' },
              { label: 'ATS Score', score: analysis.ats_score, color: '#06B6D4' },
              { label: 'Technical Depth', score: analysis.skills_score, color: '#10B981' },
              { label: 'Project Impact', score: analysis.project_score, color: '#8B5CF6' },
              { label: 'Experience Alignment', score: analysis.experience_score, color: '#F59E0B' },
              { label: 'Formatting & Layout', score: analysis.formatting_score, color: '#EC4899' },
            ].map((card, i) => (
              <div key={i} className="p-4 rounded-2xl glass-panel flex flex-col items-center justify-between text-center">
                <ProgressRing percentage={card.score} size={64} strokeWidth={5} color={card.color} />
                <span className="text-xs font-bold text-slate-200 mt-2 block">{card.label}</span>
              </div>
            ))}
          </div>

          {/* Strengths, Weaknesses, and Actionable Suggestions */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Strengths */}
            <div className="p-6 rounded-3xl glass-panel space-y-4">
              <div className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-5 h-5" />
                <h3 className="text-base font-bold font-heading text-white">Identified Strengths</h3>
              </div>
              <ul className="space-y-2.5">
                {analysis.strengths?.map((s, idx) => (
                  <li key={idx} className="p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/15 text-xs text-slate-200 flex items-start gap-2">
                    <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Weaknesses & Missing Items */}
            <div className="p-6 rounded-3xl glass-panel space-y-4">
              <div className="flex items-center gap-2 text-rose-400">
                <AlertCircle className="w-5 h-5" />
                <h3 className="text-base font-bold font-heading text-white">Areas for Improvement</h3>
              </div>
              <ul className="space-y-2.5">
                {analysis.weaknesses?.map((w, idx) => (
                  <li key={idx} className="p-3 rounded-xl bg-rose-500/5 border border-rose-500/15 text-xs text-slate-200 flex items-start gap-2">
                    <span className="text-rose-400 font-bold mt-0.5">!</span>
                    <span>{w}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* AI Bullet Point Optimizer (Google XYZ Formula) */}
          <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-indigo-500/30 space-y-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold font-heading text-white">
                  AI Quantified Bullet Point Optimizer
                </h3>
                <p className="text-xs text-slate-400">
                  Rewritten using Google's XYZ formula: "Accomplished [X] as measured by [Y], by doing [Z]"
                </p>
              </div>
            </div>

            <div className="space-y-4">
              {analysis.improved_bullets?.map((bullet, idx) => (
                <div key={idx} className="p-5 rounded-2xl bg-white/3 border border-white/8 space-y-3">
                  {/* Before */}
                  <div>
                    <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider block mb-1">
                      Original Descriptive Bullet:
                    </span>
                    <p className="text-xs text-slate-400 bg-rose-500/5 p-3 rounded-xl border border-rose-500/15">
                      "{bullet.original}"
                    </p>
                  </div>

                  {/* After */}
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">
                        Optimized High-Impact Rewrite:
                      </span>
                      <button
                        onClick={() => handleCopyBullet(bullet.improved, idx)}
                        className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 font-semibold"
                      >
                        {copiedIdx === idx ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                        {copiedIdx === idx ? 'Copied' : 'Copy'}
                      </button>
                    </div>
                    <p className="text-xs text-white font-medium bg-emerald-500/10 p-3 rounded-xl border border-emerald-500/30 leading-relaxed">
                      "{bullet.improved}"
                    </p>
                  </div>

                  {/* Rationale */}
                  <p className="text-[11px] text-slate-400 italic">
                    💡 <strong>Why this works:</strong> {bullet.rationale}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
