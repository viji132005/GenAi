import React, { useState, useEffect } from 'react';
import {
  UserCheck,
  GraduationCap,
  Code2,
  Target,
  Save,
  Plus,
  Trash2,
  CheckCircle2,
  Sparkles,
  Briefcase,
  Layers,
  FolderGit2
} from 'lucide-react';
import { profileAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import LoadingState from '../components/ui/LoadingState';

export default function ProfileSettingsPage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [activeTab, setActiveTab] = useState('profile'); // 'profile' | 'skills' | 'career'

  // New skill input
  const [newSkillName, setNewSkillName] = useState('');
  const [newSkillCategory, setNewSkillCategory] = useState('Languages');
  const [newSkillProficiency, setNewSkillProficiency] = useState('Intermediate');

  // New interest tag input
  const [newInterest, setNewInterest] = useState('');

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const pRes = await profileAPI.getProfile();
      setProfile(pRes.data);
    } catch (e) {
      console.error('Error loading student profile', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await profileAPI.updateProfile(profile);
      setProfile(res.data);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (e) {
      console.error(e);
      alert('Failed to save profile changes');
    } finally {
      setSaving(false);
    }
  };

  const handleAddSkill = async (e) => {
    e.preventDefault();
    if (!newSkillName.trim()) return;

    try {
      const res = await profileAPI.addSkill({
        name: newSkillName.trim(),
        category: newSkillCategory,
        proficiency_level: newSkillProficiency
      });
      setProfile((prev) => ({
        ...prev,
        skills: [...prev.skills, res.data]
      }));
      setNewSkillName('');
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteSkill = async (skillId) => {
    try {
      await profileAPI.deleteSkill(skillId);
      setProfile((prev) => ({
        ...prev,
        skills: prev.skills.filter((s) => s.id !== skillId)
      }));
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddInterest = (e) => {
    e.preventDefault();
    if (!newInterest.trim()) return;
    const current = profile.interests || [];
    if (!current.includes(newInterest.trim())) {
      setProfile({ ...profile, interests: [...current, newInterest.trim()] });
    }
    setNewInterest('');
  };

  const handleRemoveInterest = (tag) => {
    const current = profile.interests || [];
    setProfile({ ...profile, interests: current.filter((t) => t !== tag) });
  };

  if (loading) {
    return <LoadingState message="Loading Student Profile..." subtext="Retrieving verified coursework and academic credentials" />;
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-2">
          <UserCheck className="w-3.5 h-3.5" />
          <span>Student Account & Profile</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
          My Profile & Preferences
        </h1>
        <p className="text-sm text-slate-400">
          Manage your academic credentials, verified technical skills, and career pathway preferences.
        </p>
      </div>

      {saveSuccess && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-sm flex items-center gap-3">
          <CheckCircle2 className="w-5 h-5 shrink-0" />
          <span>Profile changes saved successfully! Career recommendations and roadmaps updated.</span>
        </div>
      )}

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-white/8 pb-4">
        <button
          onClick={() => setActiveTab('profile')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            activeTab === 'profile' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
          }`}
        >
          <GraduationCap className="w-4 h-4" /> Academic Profile
        </button>
        <button
          onClick={() => setActiveTab('skills')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            activeTab === 'skills' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Code2 className="w-4 h-4" /> Technical Skills ({profile?.skills?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('career')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            activeTab === 'career' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Target className="w-4 h-4" /> Career & Preferences
        </button>
      </div>

      {/* TAB 1: ACADEMIC PROFILE */}
      {activeTab === 'profile' && profile && (
        <form onSubmit={handleSaveProfile} className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 space-y-6 shadow-2xl">
          <div className="grid sm:grid-cols-2 gap-5">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">College / University</label>
              <input
                type="text"
                value={profile.college || ''}
                onChange={(e) => setProfile({ ...profile, college: e.target.value })}
                placeholder="e.g. National Institute of Technology"
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Target Career Goal</label>
              <input
                type="text"
                value={profile.target_career || ''}
                onChange={(e) => setProfile({ ...profile, target_career: e.target.value })}
                placeholder="e.g. AI/ML Engineer"
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-5">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Degree</label>
              <input
                type="text"
                value={profile.degree || ''}
                onChange={(e) => setProfile({ ...profile, degree: e.target.value })}
                placeholder="e.g. Bachelor of Technology (B.Tech)"
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Branch / Specialization</label>
              <input
                type="text"
                value={profile.branch || ''}
                onChange={(e) => setProfile({ ...profile, branch: e.target.value })}
                placeholder="e.g. Computer Science & Engineering"
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-5">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Semester</label>
              <input
                type="number"
                min="1"
                max="8"
                value={profile.semester || 1}
                onChange={(e) => setProfile({ ...profile, semester: parseInt(e.target.value) || 1 })}
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Graduation Year</label>
              <input
                type="number"
                value={profile.graduation_year || 2026}
                onChange={(e) => setProfile({ ...profile, graduation_year: parseInt(e.target.value) || 2026 })}
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">CGPA (out of 10)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                value={profile.cgpa || 0}
                onChange={(e) => setProfile({ ...profile, cgpa: parseFloat(e.target.value) || 0 })}
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-white/8">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2 disabled:opacity-50"
            >
              <Save className="w-4 h-4" />
              {saving ? 'Saving...' : 'Save Profile Changes'}
            </button>
          </div>
        </form>
      )}

      {/* TAB 2: TECHNICAL SKILLS */}
      {activeTab === 'skills' && profile && (
        <div className="space-y-6">
          {/* Add Skill Form */}
          <form onSubmit={handleAddSkill} className="glass-panel p-6 rounded-3xl border border-white/10 flex flex-col sm:flex-row items-end gap-3">
            <div className="flex-1 w-full">
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Skill Name</label>
              <input
                type="text"
                required
                value={newSkillName}
                onChange={(e) => setNewSkillName(e.target.value)}
                placeholder="e.g. PyTorch, Docker, Kubernetes, FastApi..."
                className="w-full px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-xs focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="w-full sm:w-44">
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Category</label>
              <select
                value={newSkillCategory}
                onChange={(e) => setNewSkillCategory(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-[#111827] border border-white/10 text-white text-xs"
              >
                <option value="Languages">Languages</option>
                <option value="AI / ML">AI / ML</option>
                <option value="Frontend">Frontend</option>
                <option value="Backend">Backend</option>
                <option value="Databases">Databases</option>
                <option value="Cloud / DevOps">Cloud / DevOps</option>
                <option value="Security">Security</option>
              </select>
            </div>

            <div className="w-full sm:w-44">
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Proficiency</label>
              <select
                value={newSkillProficiency}
                onChange={(e) => setNewSkillProficiency(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-[#111827] border border-white/10 text-white text-xs"
              >
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>

            <button
              type="submit"
              className="px-6 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center gap-1.5 shrink-0"
            >
              <Plus className="w-4 h-4" /> Add Skill
            </button>
          </form>

          {/* Current Skills Table */}
          <div className="glass-panel rounded-3xl border border-white/10 overflow-hidden">
            <div className="p-5 border-b border-white/8 flex items-center justify-between">
              <h3 className="text-base font-bold font-heading text-white">
                Verified Technical Skills ({profile.skills?.length || 0})
              </h3>
            </div>

            <div className="divide-y divide-white/5">
              {profile.skills && profile.skills.length > 0 ? (
                profile.skills.map((s) => (
                  <div key={s.id} className="p-4 flex items-center justify-between hover:bg-white/2 transition-colors">
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-semibold text-white">{s.name}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded bg-white/5 text-slate-400 font-medium">
                        {s.category}
                      </span>
                    </div>

                    <div className="flex items-center gap-4">
                      <span
                        className={`text-xs font-semibold px-2.5 py-0.5 rounded-full ${
                          s.proficiency_level === 'Advanced'
                            ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
                            : s.proficiency_level === 'Intermediate'
                            ? 'bg-indigo-500/15 text-indigo-300 border border-indigo-500/30'
                            : 'bg-slate-700/50 text-slate-300 border border-slate-600'
                        }`}
                      >
                        {s.proficiency_level}
                      </span>
                      <button
                        onClick={() => handleDeleteSkill(s.id)}
                        className="p-1 text-slate-500 hover:text-rose-400 transition-colors"
                        title="Remove Skill"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-8 text-center text-slate-400 text-xs">
                  No technical skills added yet. Add your core competencies above.
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: CAREER GOALS & PREFERENCES */}
      {activeTab === 'career' && profile && (
        <form onSubmit={handleSaveProfile} className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 space-y-6 shadow-2xl">
          <div className="flex items-center gap-3 border-b border-white/8 pb-4">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold font-heading text-white">Career Goals & Industry Interests</h2>
              <p className="text-xs text-slate-400">Tailor AI recommendations and skill roadmap generation</p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Primary Target Role</label>
              <input
                type="text"
                value={profile.target_career || ''}
                onChange={(e) => setProfile({ ...profile, target_career: e.target.value })}
                placeholder="e.g. AI/ML Engineer, Full Stack Developer, Data Scientist..."
                className="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Interests & Specializations</label>
              <div className="flex flex-wrap gap-2 mb-3">
                {(profile.interests || ['Deep Learning', 'Computer Vision', 'MLOps', 'Distributed Systems']).map((tag, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold flex items-center gap-1.5"
                  >
                    {tag}
                    <button
                      type="button"
                      onClick={() => handleRemoveInterest(tag)}
                      className="hover:text-rose-400"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={newInterest}
                  onChange={(e) => setNewInterest(e.target.value)}
                  placeholder="Add an interest (e.g. LLMs, Cloud Infrastructure, Generative AI)"
                  className="flex-1 px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-xs focus:outline-none focus:border-indigo-500"
                />
                <button
                  type="button"
                  onClick={handleAddInterest}
                  className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-semibold"
                >
                  Add Tag
                </button>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-white/8">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 rounded-xl btn-primary text-xs font-bold text-white flex items-center gap-2 disabled:opacity-50"
            >
              <Save className="w-4 h-4" />
              {saving ? 'Saving...' : 'Save Career Preferences'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
