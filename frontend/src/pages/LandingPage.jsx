import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  Sparkles,
  ArrowRight,
  Target,
  Compass,
  GitPullRequest,
  Map,
  FileText,
  Briefcase,
  Mic,
  BarChart3,
  CheckCircle2,
  Cpu,
  Layers,
  GraduationCap,
  ShieldCheck,
  Code2
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LandingPage() {
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();

  const handleDemoLogin = async () => {
    try {
      await login('demo@skillbridge.ai', 'password123');
      navigate('/dashboard');
    } catch (e) {
      navigate('/login');
    }
  };

  return (
    <div className="min-h-screen bg-[#090D16] text-white flex flex-col selection:bg-indigo-500 selection:text-white">
      {/* Background glow decorations */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-indigo-600/15 rounded-full blur-[160px] pointer-events-none -z-10" />
      <div className="fixed top-1/3 right-10 w-[400px] h-[400px] bg-cyan-500/10 rounded-full blur-[140px] pointer-events-none -z-10" />

      {/* Top Navbar */}
      <header className="border-b border-white/8 backdrop-blur-md sticky top-0 z-50 bg-[#090D16]/80">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 p-0.5 shadow-lg shadow-indigo-500/25">
              <div className="w-full h-full bg-[#090D16] rounded-[10px] flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-indigo-400" />
              </div>
            </div>
            <span className="text-2xl font-bold font-heading bg-gradient-to-r from-white via-indigo-100 to-indigo-300 bg-clip-text text-transparent">
              SkillBridge <span className="text-indigo-400">AI</span>
            </span>
          </div>

          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <NavLink to="/dashboard" className="px-5 py-2.5 rounded-xl btn-primary text-sm font-semibold flex items-center gap-2">
                Open Dashboard <ArrowRight className="w-4 h-4" />
              </NavLink>
            ) : (
              <>
                <button
                  onClick={handleDemoLogin}
                  className="hidden sm:flex px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 hover:bg-indigo-500/20 transition-colors items-center gap-1.5"
                >
                  <Cpu className="w-3.5 h-3.5 text-indigo-400" />
                  Instant Student Tour
                </button>
                <NavLink to="/login" className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white transition-colors">
                  Log in
                </NavLink>
                <NavLink to="/register" className="px-5 py-2.5 rounded-xl btn-primary text-sm font-semibold">
                  Get Started
                </NavLink>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-24 px-6 max-w-7xl mx-auto text-center flex flex-col items-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-panel border border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-8 animate-ai-pulse">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>The Next-Gen Career Navigation Platform for Engineering Students</span>
        </div>

        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold font-heading tracking-tight max-w-5xl leading-[1.15] mb-6">
          Bridge the gap between your <span className="bg-gradient-to-r from-indigo-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">skills</span> and your <span className="bg-gradient-to-r from-cyan-400 via-indigo-300 to-indigo-500 bg-clip-text text-transparent">dream career</span>.
        </h1>

        <p className="text-lg sm:text-xl text-slate-300 max-w-3xl mb-10 leading-relaxed font-normal">
          Understand where you are, discover where you can go, and get a personalized AI-powered roadmap to become 100% job-ready. Not a generic chatbot — a true career co-pilot.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4 mb-16">
          <NavLink to="/register" className="w-full sm:w-auto px-8 py-4 rounded-xl btn-primary text-base font-bold flex items-center justify-center gap-2.5">
            Start Your Free Assessment <ArrowRight className="w-5 h-5" />
          </NavLink>
          <button
            onClick={handleDemoLogin}
            className="w-full sm:w-auto px-8 py-4 rounded-xl btn-secondary text-base font-semibold text-slate-200 hover:text-white flex items-center justify-center gap-2"
          >
            <Cpu className="w-5 h-5 text-cyan-400" />
            Instant Student Preview
          </button>
        </div>

        {/* The Central Career Loop Diagram */}
        <div className="w-full max-w-5xl glass-panel rounded-2xl p-6 sm:p-8 border border-white/10 relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 via-cyan-400 to-emerald-400" />
          <h3 className="text-xs uppercase tracking-widest text-indigo-300 font-bold mb-6">The SkillBridge Intelligent Loop</h3>
          
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
            {[
              { step: '01', title: 'Student Profile', desc: 'Academics, validated skills & interests', icon: GraduationCap, color: 'text-indigo-400' },
              { step: '02', title: 'AI Match & Gap', desc: 'Deep taxonomy & requirement comparison', icon: GitPullRequest, color: 'text-cyan-400' },
              { step: '03', title: 'Curated Roadmap', desc: 'Milestone tasks & real projects', icon: Map, color: 'text-emerald-400' },
              { step: '04', title: 'Resume & Job Fit', desc: 'ATS audit & compatibility scores', icon: FileText, color: 'text-amber-400' },
              { step: '05', title: 'Interview Ready', desc: 'Live multi-turn mock interviews', icon: Mic, color: 'text-rose-400' },
            ].map((item, idx) => {
              const Icon = item.icon;
              return (
                <div key={idx} className="p-4 rounded-xl bg-white/3 border border-white/5 flex flex-col items-center text-center">
                  <div className={`w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center mb-3 ${item.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] font-bold text-slate-500 tracking-wider mb-1">STEP {item.step}</span>
                  <h4 className="text-sm font-bold text-white mb-1">{item.title}</h4>
                  <p className="text-xs text-slate-400 leading-snug">{item.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Problem vs Solution Section */}
      <section className="py-20 px-6 border-t border-white/8 bg-[#0B0F1B]/70">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl sm:text-4xl font-extrabold font-heading mb-4">
              The College-to-Career Disconnect Solved
            </h2>
            <p className="text-slate-400 text-base">
              Why traditional career advice fails college students, and how SkillBridge AI changes the paradigm.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* The Old Way */}
            <div className="p-8 rounded-2xl bg-rose-500/5 border border-rose-500/20 flex flex-col justify-between">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 text-rose-400 text-xs font-bold mb-6">
                  ✕ The Traditional Problem
                </div>
                <ul className="space-y-4 text-sm text-slate-300">
                  <li className="flex items-start gap-3">
                    <span className="text-rose-400 font-bold mt-0.5">✗</span>
                    <span><strong>Generic Chatbots:</strong> Give vague suggestions without knowing your coursework, semester, or real GitHub projects.</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-rose-400 font-bold mt-0.5">✗</span>
                    <span><strong>Unclear Skill Gaps:</strong> Students know they want to be an "AI Engineer" but don't know the exact missing industry stack.</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-rose-400 font-bold mt-0.5">✗</span>
                    <span><strong>Cookie-cutter Projects:</strong> Building standard To-Do apps that get rejected by modern technical recruiters.</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-rose-400 font-bold mt-0.5">✗</span>
                    <span><strong>Blind Job Applications:</strong> Applying to hundreds of jobs without knowing your actual compatibility score.</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* The SkillBridge Way */}
            <div className="p-8 rounded-2xl bg-indigo-500/5 border border-indigo-500/30 flex flex-col justify-between shadow-lg shadow-indigo-500/10">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-bold mb-6">
                  ✓ The SkillBridge AI Advantage
                </div>
                <ul className="space-y-4 text-sm text-slate-200">
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                    <span><strong>Grounded Intelligence:</strong> Every answer is synthesized with your verified profile, CGPA, and career goal in context.</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                    <span><strong>Actionable Skill Matrix:</strong> Prioritizes gaps into High, Medium, and Low with realistic study weeks and resources.</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                    <span><strong>Production Project Blueprints:</strong> Personalized architecture plans with Google XYZ resume bullet formulations.</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                    <span><strong>Interactive Mock Interviews:</strong> Real-time technical & behavioral simulation with pointed follow-up questions.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-400 mb-2 block">Comprehensive Suite</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold font-heading mb-4">
            Everything you need to become job-ready
          </h2>
          <p className="text-slate-400 text-base">
            From the first day of college to your final technical interview offer.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              title: "Career Match Engine",
              desc: "Evaluates your academic background, skills, and projects against 9+ tech pathways to calculate realistic match percentages.",
              icon: Compass,
              color: "text-indigo-400"
            },
            {
              title: "Skill Gap Diagnostics",
              desc: "Compares your skills against industry standards, categorizing gaps into High, Medium, and Low priority with time estimates.",
              icon: GitPullRequest,
              color: "text-cyan-400"
            },
            {
              title: "Personalized Roadmap",
              desc: "Generates a 6-phase milestone curriculum with tracked checklists, official resource links, and project checkpoints.",
              icon: Map,
              color: "text-emerald-400"
            },
            {
              title: "Resume & ATS Optimizer",
              desc: "Upload your PDF resume to receive an ATS audit, section score breakdowns, and quantified Google XYZ bullet rewrites.",
              icon: FileText,
              color: "text-amber-400"
            },
            {
              title: "Job Match Analyzer",
              desc: "Paste any real-world job description to calculate exact match %, missing requirements, and a 3-step action plan.",
              icon: Briefcase,
              color: "text-purple-400"
            },
            {
              title: "AI Mock Interview Room",
              desc: "Practice multi-turn technical and behavioral rounds with real-time scoring, constructive critiques, and final report cards.",
              icon: Mic,
              color: "text-rose-400"
            },
          ].map((f, i) => {
            const Icon = f.icon;
            return (
              <div key={i} className="p-7 rounded-2xl glass-panel glass-panel-hover flex flex-col justify-between">
                <div>
                  <div className={`w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-5 ${f.color}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-bold font-heading text-white mb-2">{f.title}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Footer CTA */}
      <section className="py-20 px-6 border-t border-white/8 bg-gradient-to-b from-[#090D16] to-[#0D1322]">
        <div className="max-w-4xl mx-auto text-center glass-panel p-10 sm:p-14 rounded-3xl border border-indigo-500/30 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
          <h2 className="text-3xl sm:text-4xl font-extrabold font-heading text-white mb-4">
            Ready to bridge your career gap?
          </h2>
          <p className="text-slate-300 text-base max-w-xl mx-auto mb-8">
            Join thousands of engineering students who are turning ambiguity into a structured, achievable roadmap.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
            <NavLink to="/register" className="px-8 py-3.5 rounded-xl btn-primary font-bold text-sm">
              Create Your Student Account
            </NavLink>
            <button onClick={handleDemoLogin} className="px-8 py-3.5 rounded-xl btn-secondary font-semibold text-sm">
              Explore Instant Tour
            </button>
          </div>
        </div>

        <div className="max-w-7xl mx-auto mt-16 pt-8 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© 2026 SkillBridge AI. Modular LLM Architecture powered by Google Gemini.</p>
          <p>Built with React, FastAPI, SQLAlchemy, and RAG Knowledge Engine.</p>
        </div>
      </section>
    </div>
  );
}
