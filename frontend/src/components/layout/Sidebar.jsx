import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  Compass,
  GitPullRequest,
  Map,
  FileText,
  Briefcase,
  FolderGit2,
  Mic,
  BotMessageSquare,
  BarChart3,
  UserCheck,
  LogOut,
  Sparkles,
  ChevronRight
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Career Analysis', path: '/career-analysis', icon: Compass },
  { name: 'Skill Gap Matrix', path: '/skill-gap', icon: GitPullRequest },
  { name: 'Career Roadmap', path: '/roadmap', icon: Map },
  { name: 'Resume & ATS', path: '/resume-analyzer', icon: FileText },
  { name: 'Job Match Analyzer', path: '/job-analyzer', icon: Briefcase },
  { name: 'Project Blueprints', path: '/projects', icon: FolderGit2 },
  { name: 'AI Mock Interview', path: '/mock-interview', icon: Mic },
  { name: 'Career Assistant', path: '/assistant', icon: BotMessageSquare, badge: 'RAG' },
  { name: 'Progress Analytics', path: '/analytics', icon: BarChart3 },
  { name: 'My Profile', path: '/profile', icon: UserCheck },
];

export default function Sidebar({ isOpen, onClose }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-72 bg-[#0C1220]/95 backdrop-blur-xl border-r border-white/8 flex flex-col transition-transform duration-300 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Header */}
        <div className="p-6 border-b border-white/8 flex items-center justify-between">
          <NavLink to="/dashboard" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 p-0.5 shadow-lg shadow-indigo-500/25 group-hover:scale-105 transition-transform">
              <div className="w-full h-full bg-[#090D16] rounded-[10px] flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-indigo-400" />
              </div>
            </div>
            <div>
              <span className="text-xl font-bold font-heading bg-gradient-to-r from-white via-indigo-100 to-indigo-300 bg-clip-text text-transparent">
                SkillBridge <span className="text-indigo-400">AI</span>
              </span>
              <p className="text-[11px] text-slate-400 tracking-wider uppercase font-medium">Career Intelligence</p>
            </div>
          </NavLink>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 px-4 py-4 space-y-1.5 overflow-y-auto">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all group ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-600/20 to-cyan-500/10 text-white border border-indigo-500/30 shadow-sm shadow-indigo-500/10'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-white/4'
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-4 h-4 transition-colors group-hover:text-indigo-400" />
                  <span>{item.name}</span>
                </div>
                {item.badge ? (
                  <span className="px-1.5 py-0.5 text-[10px] font-semibold tracking-wider rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    {item.badge}
                  </span>
                ) : (
                  <ChevronRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-60 transition-opacity" />
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* User Card & Logout */}
        <div className="p-4 border-t border-white/8 bg-[#090D16]/60">
          <div className="flex items-center justify-between p-2 rounded-xl glass-panel">
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-9 h-9 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center font-bold text-indigo-300 text-sm">
                {user?.full_name?.charAt(0) || 'U'}
              </div>
              <div className="min-w-0">
                <p className="text-sm font-semibold text-white truncate">{user?.full_name || 'Student'}</p>
                <p className="text-xs text-slate-400 truncate">{user?.email || 'demo@skillbridge.ai'}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              title="Logout"
              className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
