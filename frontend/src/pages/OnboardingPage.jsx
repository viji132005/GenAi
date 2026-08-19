import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles,
  GraduationCap,
  Code2,
  Compass,
  Award,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  Plus,
  Trash2,
  AlertCircle
} from 'lucide-react';
import { profileAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const COMMON_SKILLS = [
  'Python', 'Java', 'C++', 'JavaScript', 'TypeScript', 'SQL', 'HTML', 'CSS',
  'React', 'Next.js', 'Node.js', 'FastAPI', 'Django',
  'Machine Learning', 'PyTorch', 'TensorFlow', 'Scikit-Learn', 'Pandas', 'NumPy',
  'PostgreSQL', 'MongoDB', 'Redis',
  'Docker', 'AWS', 'Kubernetes', 'Git', 'Linux'
];

const CAREER_OPTIONS = [
  'AI/ML Engineer',
  'Data Scientist',
  'Data Analyst',
  'Full Stack Developer',
  'Backend Developer',
  'Frontend Developer',
  'Cloud / DevOps Engineer',
  'Cybersecurity Analyst',
  'Mobile App Developer'
];

const INTEREST_OPTIONS = [
  'Artificial Intelligence', 'Machine Learning', 'Deep Learning',
  'Web Development', 'Cloud Computing', 'Data Science',
  'Cybersecurity', 'DevOps & CI/CD', 'Mobile Apps', 'Distributed Systems'
];

export default function OnboardingPage() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { refreshUser } = useAuth();
  const navigate = useNavigate();

  // Form State
  const [formData, setFormData] = useState({
    college: 'National Institute of Technology',
    degree: 'B.E.',
    branch: 'Computer Science & Engineering',
    semester: 6,
    graduation_year: 2026,
    cgpa: 7.8,
    target_career: 'AI/ML Engineer',
    interests: ['Artificial Intelligence', 'Machine Learning', 'Web Development'],
    skills: [
      { name: 'Python', category: 'Languages', proficiency_level: 'Intermediate' },
      { name: 'SQL', category: 'Databases', proficiency_level: 'Intermediate' },
      { name: 'JavaScript', category: 'Languages', proficiency_level: 'Intermediate' },
      { name: 'HTML', category: 'Frontend', proficiency_level: 'Intermediate' },
      { name: 'CSS', category: 'Frontend', proficiency_level: 'Intermediate' },
      { name: 'Machine Learning', category: 'AI / ML', proficiency_level: 'Beginner' }
    ],
    coursework: [
      'Data Structures & Algorithms',
      'Database Management Systems',
      'Operating Systems',
      'Probability & Statistics'
    ],
    achievements: ['Finalist at University Hackathon 2025']
  });

  const [customSkill, setCustomSkill] = useState('');
  const [customProficiency, setCustomProficiency] = useState('Beginner');

  const handleToggleInterest = (item) => {
    setFormData((prev) => {
      const exists = prev.interests.includes(item);
      return {
        ...prev,
        interests: exists ? prev.interests.filter((i) => i !== item) : [...prev.interests, item]
      };
    });
  };

  const handleAddPredefinedSkill = (skillName) => {
    if (formData.skills.some((s) => s.name.toLowerCase() === skillName.toLowerCase())) return;
    setFormData((prev) => ({
      ...prev,
      skills: [...prev.skills, { name: skillName, category: 'Technical', proficiency_level: 'Intermediate' }]
    }));
  };

  const handleAddCustomSkill = (e) => {
    e.preventDefault();
    if (!customSkill.trim()) return;
    if (formData.skills.some((s) => s.name.toLowerCase() === customSkill.toLowerCase())) return;
    setFormData((prev) => ({
      ...prev,
      skills: [...prev.skills, { name: customSkill.trim(), category: 'Technical', proficiency_level: customProficiency }]
    }));
    setCustomSkill('');
  };

  const handleRemoveSkill = (skillName) => {
    setFormData((prev) => ({
      ...prev,
      skills: prev.skills.filter((s) => s.name !== skillName)
    }));
  };

  const handleProficiencyChange = (skillName, newLevel) => {
    setFormData((prev) => ({
      ...prev,
      skills: prev.skills.map((s) => (s.name === skillName ? { ...s, proficiency_level: newLevel } : s))
    }));
  };

  const handleComplete = async () => {
    setError('');
    setLoading(true);
    try {
      await profileAPI.completeOnboarding(formData);
      await refreshUser();
      navigate('/dashboard');
    } catch (e) {
      console.error('Onboarding submission failed', e);
      setError(e.response?.data?.detail || 'Failed to complete profile activation. Please check the backend connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#090D16] text-white flex flex-col items-center justify-center p-4 sm:p-6 relative overflow-hidden">
      {/* Background glow */}
      <div className="fixed top-1/3 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-indigo-600/10 rounded-full blur-[160px] pointer-events-none" />

      <div className="w-full max-w-2xl relative z-10">
        {/* Step Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400 mb-3">
            <span>STEP {step} OF 4</span>
            <span className="text-indigo-400">
              {step === 1 && 'Academics & College'}
              {step === 2 && 'Technical Skills'}
              {step === 3 && 'Career Goal & Interests'}
              {step === 4 && 'Experience & Review'}
            </span>
          </div>
          <div className="w-full h-2 rounded-full bg-white/10 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 transition-all duration-300 rounded-full"
              style={{ width: `${(step / 4) * 100}%` }}
            />
          </div>
        </div>

        {/* Wizard Card Container */}
        <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 shadow-2xl">
          {error && (
            <div className="mb-5 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-2.5 text-xs text-rose-300">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
          {/* STEP 1: Personal & College Info */}
          {step === 1 && (
            <div className="space-y-5 animate-in fade-in duration-300">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold font-heading text-white">Academic Background</h2>
                  <p className="text-xs text-slate-400">Tell us where you are currently studying</p>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">College / University Name</label>
                <input
                  type="text"
                  value={formData.college}
                  onChange={(e) => setFormData({ ...formData, college: e.target.value })}
                  placeholder="e.g. National Institute of Technology"
                  className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">Degree</label>
                  <input
                    type="text"
                    value={formData.degree}
                    onChange={(e) => setFormData({ ...formData, degree: e.target.value })}
                    placeholder="e.g. B.E. / B.Tech / B.S."
                    className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">Branch / Major</label>
                  <input
                    type="text"
                    value={formData.branch}
                    onChange={(e) => setFormData({ ...formData, branch: e.target.value })}
                    placeholder="e.g. Computer Science & Eng"
                    className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">Current Semester</label>
                  <select
                    value={formData.semester}
                    onChange={(e) => setFormData({ ...formData, semester: parseInt(e.target.value) })}
                    className="w-full px-3 py-2.5 rounded-xl bg-[#111827] border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                  >
                    {[1, 2, 3, 4, 5, 6, 7, 8].map((sem) => (
                      <option key={sem} value={sem}>Semester {sem}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">Graduation Year</label>
                  <input
                    type="number"
                    value={formData.graduation_year}
                    onChange={(e) => setFormData({ ...formData, graduation_year: parseInt(e.target.value) })}
                    className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">CGPA (out of 10)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="10"
                    value={formData.cgpa}
                    onChange={(e) => setFormData({ ...formData, cgpa: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: Technical Skills */}
          {step === 2 && (
            <div className="space-y-5 animate-in fade-in duration-300">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center">
                  <Code2 className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold font-heading text-white">Your Technical Skills</h2>
                  <p className="text-xs text-slate-400">Add your current languages, frameworks, and databases</p>
                </div>
              </div>

              {/* Selected Skills List */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-2">
                  Selected Skills ({formData.skills.length})
                </label>
                <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                  {formData.skills.map((sk) => (
                    <div key={sk.name} className="flex items-center justify-between p-2.5 rounded-xl bg-white/5 border border-white/8">
                      <span className="text-sm font-semibold text-white">{sk.name}</span>
                      <div className="flex items-center gap-3">
                        <select
                          value={sk.proficiency_level}
                          onChange={(e) => handleProficiencyChange(sk.name, e.target.value)}
                          className="px-2.5 py-1 text-xs rounded-lg bg-[#111827] border border-white/10 text-slate-200"
                        >
                          <option value="Beginner">Beginner</option>
                          <option value="Intermediate">Intermediate</option>
                          <option value="Advanced">Advanced</option>
                        </select>
                        <button
                          type="button"
                          onClick={() => handleRemoveSkill(sk.name)}
                          className="text-slate-500 hover:text-rose-400 transition-colors p-1"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Add Tag Suggestions */}
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1.5">Quick Add Popular Technologies</label>
                <div className="flex flex-wrap gap-1.5">
                  {COMMON_SKILLS.filter((s) => !formData.skills.some((sk) => sk.name.toLowerCase() === s.toLowerCase())).map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => handleAddPredefinedSkill(s)}
                      className="px-2.5 py-1 rounded-lg text-xs font-medium bg-white/5 border border-white/8 text-slate-300 hover:border-indigo-500 hover:text-indigo-300 transition-colors flex items-center gap-1"
                    >
                      <Plus className="w-3 h-3" /> {s}
                    </button>
                  ))}
                </div>
              </div>

              {/* Custom Skill Input */}
              <div className="pt-2 border-t border-white/8">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={customSkill}
                    onChange={(e) => setCustomSkill(e.target.value)}
                    placeholder="Type custom skill..."
                    className="flex-1 px-3.5 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-xs focus:outline-none focus:border-indigo-500"
                  />
                  <select
                    value={customProficiency}
                    onChange={(e) => setCustomProficiency(e.target.value)}
                    className="px-3 py-2 text-xs rounded-xl bg-[#111827] border border-white/10 text-white"
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                  <button
                    type="button"
                    onClick={handleAddCustomSkill}
                    className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold"
                  >
                    Add
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: Career Goal & Interests */}
          {step === 3 && (
            <div className="space-y-5 animate-in fade-in duration-300">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
                  <Compass className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold font-heading text-white">Target Career & Interests</h2>
                  <p className="text-xs text-slate-400">Select your aspiration to tailor roadmaps and gap analyses</p>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-2">Primary Target Career Goal</label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                  {CAREER_OPTIONS.map((c) => {
                    const isSelected = formData.target_career === c;
                    return (
                      <button
                        key={c}
                        type="button"
                        onClick={() => setFormData({ ...formData, target_career: c })}
                        className={`p-3 rounded-xl text-xs font-semibold text-left transition-all border ${
                          isSelected
                            ? 'bg-indigo-600/25 border-indigo-500 text-white shadow-sm shadow-indigo-500/20'
                            : 'bg-white/5 border-white/8 text-slate-300 hover:border-white/20'
                        }`}
                      >
                        {c}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-2">Engineering Interests</label>
                <div className="flex flex-wrap gap-2">
                  {INTEREST_OPTIONS.map((item) => {
                    const isSelected = formData.interests.includes(item);
                    return (
                      <button
                        key={item}
                        type="button"
                        onClick={() => handleToggleInterest(item)}
                        className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border ${
                          isSelected
                            ? 'bg-cyan-500/20 border-cyan-500 text-cyan-300'
                            : 'bg-white/5 border-white/8 text-slate-400 hover:border-white/20'
                        }`}
                      >
                        {isSelected ? '✓ ' : '+ '} {item}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* STEP 4: Review & Finalize */}
          {step === 4 && (
            <div className="space-y-5 animate-in fade-in duration-300">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center">
                  <Award className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold font-heading text-white">Profile Summary & Activation</h2>
                  <p className="text-xs text-slate-400">Review your profile before initializing the AI engine</p>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-3 text-xs">
                <div className="flex justify-between border-b border-white/5 pb-2">
                  <span className="text-slate-400">Target Career:</span>
                  <span className="font-bold text-indigo-300">{formData.target_career}</span>
                </div>
                <div className="flex justify-between border-b border-white/5 pb-2">
                  <span className="text-slate-400">Education:</span>
                  <span className="font-semibold text-white">{formData.degree} ({formData.branch}) - Sem {formData.semester}</span>
                </div>
                <div className="flex justify-between border-b border-white/5 pb-2">
                  <span className="text-slate-400">CGPA:</span>
                  <span className="font-semibold text-emerald-400">{formData.cgpa} / 10</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-1.5">Registered Skills ({formData.skills.length}):</span>
                  <div className="flex flex-wrap gap-1.5">
                    {formData.skills.map((s) => (
                      <span key={s.name} className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-[11px]">
                        {s.name} ({s.proficiency_level})
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center gap-3">
                <Sparkles className="w-5 h-5 text-indigo-400 shrink-0" />
                <p className="text-xs text-indigo-200">
                  Upon completion, SkillBridge AI will compute your initial career match scores, diagnose missing requirements, and generate your customized 6-month roadmap.
                </p>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between mt-8 pt-6 border-t border-white/8">
            {step > 1 ? (
              <button
                type="button"
                onClick={() => setStep((s) => s - 1)}
                className="px-5 py-2.5 rounded-xl btn-secondary text-xs font-semibold text-slate-300 flex items-center gap-2"
              >
                <ArrowLeft className="w-4 h-4" /> Back
              </button>
            ) : <div />}

            {step < 4 ? (
              <button
                type="button"
                onClick={() => setStep((s) => s + 1)}
                className="px-6 py-2.5 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2"
              >
                Next Step <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                disabled={loading}
                onClick={handleComplete}
                className="px-8 py-3 rounded-xl btn-primary text-sm font-bold text-white flex items-center gap-2 disabled:opacity-50"
              >
                {loading ? 'Initializing AI Engine...' : 'Generate Career Intelligence'}
                <Sparkles className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
