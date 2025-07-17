import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData: any) => api.post('/auth/register', userData),
  login: (credentials: any) => api.post('/auth/login', credentials),
  getProfile: () => api.get('/auth/profile'),
};

// Tournament API
export const tournamentAPI = {
  getTournaments: () => api.get('/tournaments'),
  createTournament: (data: any) => api.post('/tournaments', data),
  getTournament: (id: string) => api.get(`/tournaments/${id}`),
  updateTournament: (id: string, data: any) => api.put(`/tournaments/${id}`, data),
  deleteTournament: (id: string) => api.delete(`/tournaments/${id}`),
  
  // Teams
  getTeams: (tournamentId: string) => api.get(`/tournaments/${tournamentId}/teams`),
  createTeam: (tournamentId: string, data: any) => api.post(`/tournaments/${tournamentId}/teams`, data),
  
  // Matches
  scheduleMatches: (tournamentId: string) => api.post(`/tournaments/${tournamentId}/schedule`),
  getMatches: (tournamentId: string) => api.get(`/tournaments/${tournamentId}/matches`),
  updateMatch: (matchId: string, data: any) => api.put(`/matches/${matchId}`, data),
  
  // Points Table
  getPointsTable: (tournamentId: string) => api.get(`/tournaments/${tournamentId}/points-table`),
};