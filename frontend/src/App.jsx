import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Layout
import AppLayout from './components/layout/AppLayout';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import OnboardingPage from './pages/OnboardingPage';
import DashboardPage from './pages/DashboardPage';
import CareerAnalysisPage from './pages/CareerAnalysisPage';
import SkillGapPage from './pages/SkillGapPage';
import RoadmapPage from './pages/RoadmapPage';
import ResumeAnalyzerPage from './pages/ResumeAnalyzerPage';
import JobAnalyzerPage from './pages/JobAnalyzerPage';
import ProjectsPage from './pages/ProjectsPage';
import MockInterviewPage from './pages/MockInterviewPage';
import AssistantPage from './pages/AssistantPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ProfileSettingsPage from './pages/ProfileSettingsPage';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return null;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
};

const PublicOnlyRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return null;
  if (isAuthenticated) return <Navigate to="/dashboard" replace />;
  return children;
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/login"
            element={
              <PublicOnlyRoute>
                <LoginPage />
              </PublicOnlyRoute>
            }
          />
          <Route
            path="/register"
            element={
              <PublicOnlyRoute>
                <RegisterPage />
              </PublicOnlyRoute>
            }
          />
          <Route
            path="/onboarding"
            element={
              <ProtectedRoute>
                <OnboardingPage />
              </ProtectedRoute>
            }
          />

          {/* Protected Application Dashboard Routes */}
          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/career-analysis" element={<CareerAnalysisPage />} />
            <Route path="/skill-gap" element={<SkillGapPage />} />
            <Route path="/roadmap" element={<RoadmapPage />} />
            <Route path="/resume-analyzer" element={<ResumeAnalyzerPage />} />
            <Route path="/job-analyzer" element={<JobAnalyzerPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/mock-interview" element={<MockInterviewPage />} />
            <Route path="/assistant" element={<AssistantPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/profile" element={<ProfileSettingsPage />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
