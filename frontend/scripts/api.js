const API = 'http://localhost:8000';

function getToken() { return localStorage.getItem('token'); }
function getUser()  { return JSON.parse(localStorage.getItem('user') || 'null'); }
function isTrainer(){ const u = getUser(); return u && u.role === 'trainer'; }

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(API + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка запроса');
  return data;
}

export const api = {
  register: (name, email, password, role) =>
    request('POST', '/api/users/register', { name, email, password, role }),
  login: (username, password) =>
    request('POST', '/api/users/login', { username, password }),
  me: () => request('GET', '/api/users/me'),

  getWorkouts: () => request('GET', '/api/workouts'),
  getWorkout: (id) => request('GET', `/api/workouts/${id}`),
  createWorkout: (title, description) =>
    request('POST', '/api/workouts', { title, description }),
  updateWorkout: (id, fields) =>
    request('PATCH', `/api/workouts/${id}`, fields),
  deleteWorkout: (id) => request('DELETE', `/api/workouts/${id}`),

  addExercise: (workoutId, data) =>
    request('POST', `/api/exercises/${workoutId}`, data),
  deleteExercise: (id) => request('DELETE', `/api/exercises/${id}`),
};

export { getToken, getUser, isTrainer };
