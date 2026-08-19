import React, { useState, useEffect } from 'react';
import {
  Mic,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  RefreshCw,
  Award,
  Clock,
  Play,
  RotateCcw,
  MessageSquare,
  BarChart2
} from 'lucide-react';
import { interviewAPI, careerAPI } from '../services/api';
import ProgressRing from '../components/ui/ProgressRing';
import LoadingState from '../components/ui/LoadingState';

export default function MockInterviewPage() {
  const [viewState, setViewState] = useState('setup'); // 'setup' | 'interviewing' | 'report'
  const [careerList, setCareerList] = useState([]);
  
  // Setup configuration
  const [selectedCareer, setSelectedCareer] = useState('AI/ML Engineer');
  const [interviewType, setInterviewType] = useState('Technical');
  const [difficulty, setDifficulty] = useState('Intermediate');
  const [totalQuestions, setTotalQuestions] = useState(3);

  // Active Session state
  const [session, setSession] = useState(null);
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [evaluating, setEvaluating] = useState(false);
  const [lastEvalResult, setLastEvalResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Final Report state
  const [report, setReport] = useState(null);

  useEffect(() => {
    const loadCareers = async () => {
      try {
        const res = await careerAPI.getCatalogs();
        setCareerList(res.data || []);
      } catch (e) {
        console.error(e);
      }
    };
    loadCareers();
  }, []);

  const handleStartInterview = async (e) => {
    e.preventDefault();
    setLoading(true);
    setLastEvalResult(null);
    setUserAnswer('');
    try {
      const res = await interviewAPI.startInterview({
        career_title: selectedCareer,
        interview_type: interviewType,
        difficulty: difficulty,
        total_questions: totalQuestions
      });
      setSession(res.data);
      setCurrentQIndex(0);
      setViewState('interviewing');
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to start interview.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async (e) => {
    e.preventDefault();
    if (!userAnswer.trim()) return;

    const currentQuestion = session.questions[currentQIndex];
    setEvaluating(true);
    try {
      const res = await interviewAPI.submitAnswer({
        interview_id: session.id,
        question_id: currentQuestion.id,
        user_answer: userAnswer
      });
      setLastEvalResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to submit answer.');
    } finally {
      setEvaluating(false);
    }
  };

  const handleNextQuestion = async () => {
    if (lastEvalResult?.is_finished || currentQIndex >= session.questions.length - 1) {
      // Complete interview and get final report
      setLoading(true);
      try {
        const res = await interviewAPI.completeInterview(session.id);
        setReport(res.data);
        setViewState('report');
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    } else {
      setCurrentQIndex((prev) => prev + 1);
      setUserAnswer('');
      setLastEvalResult(null);
    }
  };

  const handleReset = () => {
    setViewState('setup');
    setSession(null);
    setReport(null);
    setLastEvalResult(null);
    setUserAnswer('');
  };

  if (loading) {
    return <LoadingState message="Interview Simulator Initializing..." subtext="Generating customized engineering interview questions with expected rubrics" />;
  }

  const currentQ = session?.questions?.[currentQIndex];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold mb-2">
            <Mic className="w-3.5 h-3.5" />
            <span>AI Mock Interview Simulator</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            Technical Mock Interview
          </h1>
          <p className="text-sm text-slate-400">
            Simulate realistic technical and behavioral interview rounds with real-time feedback and rubric scoring.
          </p>
        </div>

        {viewState !== 'setup' && (
          <button
            onClick={handleReset}
            className="px-4 py-2 rounded-xl btn-secondary text-xs font-semibold text-slate-200 hover:text-white flex items-center gap-2"
          >
            <RotateCcw className="w-3.5 h-3.5" /> Start New Session
          </button>
        )}
      </div>

      {/* VIEW 1: SETUP SCREEN */}
      {viewState === 'setup' && (
        <div className="glass-panel p-6 sm:p-10 rounded-3xl border border-white/10 max-w-3xl mx-auto shadow-2xl space-y-6">
          <div className="flex items-center gap-3 border-b border-white/8 pb-4">
            <div className="w-10 h-10 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center">
              <Play className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold font-heading text-white">Configure Your Interview Simulation</h2>
              <p className="text-xs text-slate-400">Select role, difficulty, and question format</p>
            </div>
          </div>

          <form onSubmit={handleStartInterview} className="space-y-5">
            {/* Target Role */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Target Career Role</label>
              <select
                value={selectedCareer}
                onChange={(e) => setSelectedCareer(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-[#111827] border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              >
                {careerList.map((c) => (
                  <option key={c.title} value={c.title}>{c.title}</option>
                ))}
              </select>
            </div>

            {/* Type & Difficulty */}
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Interview Format</label>
                <select
                  value={interviewType}
                  onChange={(e) => setInterviewType(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#111827] border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="Technical">Technical & Algorithm Concepts</option>
                  <option value="System Design">System Design & Architecture</option>
                  <option value="Behavioral">Behavioral (STAR Method)</option>
                  <option value="Mixed">Mixed Comprehensive</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Difficulty Level</label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#111827] border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="Beginner">Beginner (Foundational Concepts)</option>
                  <option value="Intermediate">Intermediate (Standard College Placement)</option>
                  <option value="Advanced">Advanced (FAANG / Product Companies)</option>
                </select>
              </div>
            </div>

            {/* Total Questions */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Number of Questions</label>
              <div className="flex gap-3">
                {[3, 4, 5].map((num) => (
                  <button
                    key={num}
                    type="button"
                    onClick={() => setTotalQuestions(num)}
                    className={`flex-1 py-2.5 rounded-xl text-xs font-bold transition-all border ${
                      totalQuestions === num
                        ? 'bg-rose-600 text-white border-rose-500 shadow-sm shadow-rose-500/25'
                        : 'bg-white/5 text-slate-400 border-white/8 hover:text-white'
                    }`}
                  >
                    {num} Questions ({num * 4} mins)
                  </button>
                ))}
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-3.5 rounded-xl bg-gradient-to-r from-rose-600 to-indigo-600 hover:from-rose-500 hover:to-indigo-500 text-white font-bold text-sm flex items-center justify-center gap-2 shadow-lg shadow-rose-600/25 transition-all mt-4"
            >
              Start Live Mock Interview Room <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}

      {/* VIEW 2: ACTIVE INTERVIEW ROOM */}
      {viewState === 'interviewing' && currentQ && (
        <div className="space-y-6 max-w-4xl mx-auto">
          {/* Header Progress */}
          <div className="flex items-center justify-between p-4 rounded-2xl glass-panel text-xs font-semibold text-slate-300">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-rose-400 animate-pulse" />
              <span>Question {currentQIndex + 1} of {session.questions.length}</span>
            </div>
            <span className="text-indigo-400 font-bold">{session.career_title} • {session.difficulty}</span>
          </div>

          {/* Question Box */}
          <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-indigo-500/30 space-y-4 shadow-xl">
            <div className="flex items-center justify-between">
              <span className="text-[10px] uppercase tracking-wider font-bold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                {currentQ.question_type} Question
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold font-heading text-white leading-snug">
              "{currentQ.question_text}"
            </h2>

            {currentQ.expected_topics?.length > 0 && (
              <div className="pt-2">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
                  Expected Discussion Points:
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {currentQ.expected_topics.map((top, idx) => (
                    <span key={idx} className="px-2 py-0.5 rounded bg-white/5 border border-white/8 text-slate-300 text-[11px]">
                      {top}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Student Answer Input */}
          {!lastEvalResult ? (
            <form onSubmit={handleSubmitAnswer} className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
              <label className="block text-xs font-semibold text-slate-300">
                Your Answer (Explain concepts, trade-offs, and examples clearly):
              </label>
              <textarea
                rows={7}
                required
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Type your structured explanation here (or paste code snippets if relevant)..."
                className="w-full p-4 rounded-2xl bg-white/5 border border-white/10 text-white text-xs font-mono focus:outline-none focus:border-indigo-500"
              />
              <div className="flex items-center justify-between pt-2">
                <span className="text-[11px] text-slate-500">{userAnswer.split(/\s+/).filter(Boolean).length} words typed</span>
                <button
                  type="submit"
                  disabled={evaluating || !userAnswer.trim()}
                  className="px-6 py-2.5 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2 disabled:opacity-50"
                >
                  {evaluating ? 'Evaluating Technical Depth...' : 'Submit Answer'}
                  <Sparkles className="w-4 h-4" />
                </button>
              </div>
            </form>
          ) : (
            /* Evaluation Result Card */
            <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-emerald-500/30 space-y-6 animate-in fade-in">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/8 pb-4">
                <div>
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 text-xs font-bold mb-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Real-time Answer Score: {lastEvalResult.score}/100</span>
                  </div>
                  <h3 className="text-lg font-bold font-heading text-white">AI Evaluator Feedback</h3>
                </div>

                <div className="flex gap-4">
                  <div className="text-center">
                    <span className="text-xs text-slate-400 block">Accuracy</span>
                    <span className="text-sm font-bold text-white">{lastEvalResult.technical_accuracy}%</span>
                  </div>
                  <div className="text-center">
                    <span className="text-xs text-slate-400 block">Completeness</span>
                    <span className="text-sm font-bold text-white">{lastEvalResult.completeness}%</span>
                  </div>
                  <div className="text-center">
                    <span className="text-xs text-slate-400 block">Clarity</span>
                    <span className="text-sm font-bold text-white">{lastEvalResult.clarity}%</span>
                  </div>
                </div>
              </div>

              {/* Feedback Content */}
              <div className="space-y-4">
                <div className="p-4 rounded-2xl bg-white/3 border border-white/5 text-xs text-slate-200 leading-relaxed">
                  <strong>Feedback:</strong> {lastEvalResult.feedback}
                </div>

                {lastEvalResult.follow_up && (
                  <div className="p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-xs text-indigo-200">
                    🔍 <strong>Follow-up Consideration:</strong> {lastEvalResult.follow_up}
                  </div>
                )}
              </div>

              <div className="flex justify-end pt-2">
                <button
                  onClick={handleNextQuestion}
                  className="px-6 py-3 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2 shadow-lg shadow-indigo-600/30"
                >
                  {lastEvalResult.is_finished || currentQIndex >= session.questions.length - 1
                    ? 'Complete Interview & View Report'
                    : 'Proceed to Next Question'}
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* VIEW 3: FINAL SCORECARD REPORT */}
      {viewState === 'report' && report && (
        <div className="space-y-8 max-w-4xl mx-auto animate-in fade-in">
          {/* Report Header Card */}
          <div className="p-8 rounded-3xl glass-panel border border-indigo-500/30 text-center space-y-6 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-indigo-500 via-cyan-400 to-emerald-400" />

            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold">
              <Award className="w-4 h-4" /> Interview Simulation Completed
            </div>

            <h2 className="text-3xl font-bold font-heading text-white">Interview Performance Scorecard</h2>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              Comprehensive evaluation of technical accuracy, communication clarity, and problem solving for {selectedCareer}.
            </p>

            {/* 3 Rings */}
            <div className="flex flex-wrap justify-center gap-8 pt-2">
              <ProgressRing percentage={report.overall_score} size={84} strokeWidth={7} color="#6366F1" label="Overall Score" />
              <ProgressRing percentage={report.technical_score} size={84} strokeWidth={7} color="#06B6D4" label="Technical Depth" />
              <ProgressRing percentage={report.communication_score} size={84} strokeWidth={7} color="#10B981" label="Communication" />
            </div>
          </div>

          {/* Strengths & Weaknesses */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="p-6 rounded-3xl glass-panel space-y-3">
              <div className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-5 h-5" />
                <h3 className="text-base font-bold font-heading text-white">Demonstrated Strengths</h3>
              </div>
              <ul className="space-y-2">
                {report.strengths?.map((st, i) => (
                  <li key={i} className="p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/15 text-xs text-slate-200 flex items-start gap-2">
                    <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                    <span>{st}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 rounded-3xl glass-panel space-y-3">
              <div className="flex items-center gap-2 text-rose-400">
                <AlertCircle className="w-5 h-5" />
                <h3 className="text-base font-bold font-heading text-white">Areas for Improvement</h3>
              </div>
              <ul className="space-y-2">
                {report.weaknesses?.map((w, i) => (
                  <li key={i} className="p-3 rounded-xl bg-rose-500/5 border border-rose-500/15 text-xs text-slate-200 flex items-start gap-2">
                    <span className="text-rose-400 font-bold mt-0.5">!</span>
                    <span>{w}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Suggestions & Topics to Revise */}
          <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-indigo-500/30 space-y-4">
            <h3 className="text-base font-bold font-heading text-white">Recommended Next Steps Before Real Interviews</h3>
            <div className="space-y-2.5">
              {report.improvement_suggestions?.map((sugg, i) => (
                <div key={i} className="p-3 rounded-xl bg-white/4 border border-white/8 text-xs text-slate-300 flex items-start gap-2.5">
                  <span className="w-5 h-5 rounded-md bg-indigo-500/20 text-indigo-400 font-bold flex items-center justify-center shrink-0">
                    {i + 1}
                  </span>
                  <span>{sugg}</span>
                </div>
              ))}
            </div>

            {report.recommended_topics?.length > 0 && (
              <div className="pt-4 border-t border-white/8">
                <span className="text-xs font-bold text-slate-400 block mb-2">Priority Revision Topics:</span>
                <div className="flex flex-wrap gap-2">
                  {report.recommended_topics.map((t, idx) => (
                    <span key={idx} className="px-3 py-1 rounded-xl bg-indigo-500/20 text-indigo-300 text-xs font-semibold border border-indigo-500/30">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="flex justify-center pt-2">
            <button
              onClick={handleReset}
              className="px-8 py-3.5 rounded-xl btn-primary text-sm font-bold text-white flex items-center gap-2 shadow-xl shadow-indigo-600/30"
            >
              <RotateCcw className="w-4 h-4" /> Practice Another Mock Interview
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
