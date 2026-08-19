import axios from 'axios';

const rawBaseURL = import.meta.env.VITE_API_URL || '/api';
const baseURL = rawBaseURL.endsWith('/') ? rawBaseURL.slice(0, -1) : rawBaseURL;

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('skillbridge_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Handle global responses & auth expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // If token expired, clear and optionally redirect
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register' && window.location.pathname !== '/') {
        localStorage.removeItem('skillbridge_token');
        localStorage.removeItem('skillbridge_user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (full_name, email, password) => api.post('/auth/register', { full_name, email, password }),
  getMe: () => api.get('/auth/me'),
};

export const profileAPI = {
  getProfile: () => api.get('/profile'),
  updateProfile: (data) => api.put('/profile', data),
  completeOnboarding: (data) => api.post('/profile/onboarding', data),
  addSkill: (skill) => api.post('/profile/skills', skill),
  deleteSkill: (skillId) => api.delete(`/profile/skills/${skillId}`),
};

export const careerAPI = {
  getCatalogs: () => api.get('/career/catalogs'),
  analyzeCareer: () => api.post('/career/analyze'),
  setTargetCareer: (career_title) => api.post('/career/set-target', { career_title }),
};

export const skillsAPI = {
  analyzeSkillGaps: (career_title) => api.post('/skills/analyze', { career_title }),
  getTaxonomy: () => api.get('/skills/taxonomy'),
};

export const roadmapAPI = {
  getRoadmap: () => api.get('/roadmap'),
  regenerateRoadmap: () => api.post('/roadmap/generate'),
  toggleTask: (taskId, is_completed) => api.put(`/roadmap/tasks/${taskId}`, { is_completed }),
};

export const resumeAPI = {
  uploadResume: (formData) => api.post('/resume/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  analyzeText: (raw_text, filename) => api.post('/resume/analyze-text', { raw_text, filename }),
  getLatest: () => api.get('/resume/latest'),
};

export const jobAPI = {
  analyzeJob: (data) => api.post('/job/analyze', data),
  getHistory: () => api.get('/job/history'),
};

export const projectsAPI = {
  getProjects: (domain, difficulty) => api.get('/projects', { params: { domain, difficulty } }),
  regenerateProjects: (domain, difficulty) => api.post('/projects/generate', {}, { params: { domain, difficulty } }),
  toggleBookmark: (projectId) => api.post(`/projects/${projectId}/bookmark`),
};

export const interviewAPI = {
  startInterview: (data) => api.post('/interview/start', data),
  submitAnswer: (data) => api.post('/interview/answer', data),
  completeInterview: (interviewId) => api.post(`/interview/${interviewId}/complete`),
  getHistory: () => api.get('/interview/history'),
  getSession: (interviewId) => api.get(`/interview/${interviewId}`),
};

export const chatAPI = {
  sendMessage: (message, conversation_id) => api.post('/chat', { message, conversation_id }),
  getConversations: () => api.get('/chat/conversations'),
};

export const analyticsAPI = {
  getDashboard: () => api.get('/analytics/dashboard'),
};

export const systemAPI = {
  getHealth: () => api.get('/health'),
  getStatus: () => api.get('/status'),
};

export default api;
