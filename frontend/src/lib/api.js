const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, { headers: { 'Content-Type': 'application/json', ...options.headers }, ...options });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || 'No fue posible completar la operación.');
  }
  return response.status === 204 ? null : response.json();
}

export const api = {
  list: (resource) => request(`/${resource}/`),
  create: (resource, data) => request(`/${resource}/`, { method: 'POST', body: JSON.stringify(data) }),
  update: (resource, id, data) => request(`/${resource}/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  remove: (resource, id) => request(`/${resource}/${id}`, { method: 'DELETE' }),
};
