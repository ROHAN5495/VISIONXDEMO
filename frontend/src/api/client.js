const BASE_URL = '/api';

async function request(endpoint, options = {}) {
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const res = await fetch(`${BASE_URL}${endpoint}`, config);
    if (!res.ok) {
      let errorMsg = `Error ${res.status}: ${res.statusText}`;
      try {
        const errorData = await res.json();
        errorMsg = errorData.detail || errorData.message || errorMsg;
      } catch (e) {
        // Fallback to text
      }
      throw new Error(errorMsg);
    }
    return await res.json();
  } catch (err) {
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      throw new Error('Unable to connect to backend service. Please check if the Evolution Tracker backend server is running on port 8000.');
    }
    throw err;
  }
}

export const api = {
  // Investigations
  getInvestigations: (params = {}) => {
    const query = new URLSearchParams();
    if (params.query) query.append('query', params.query);
    if (params.verdict) query.append('verdict', params.verdict);
    if (params.is_demo !== undefined) query.append('is_demo', params.is_demo);
    const qs = query.toString() ? `?${query.toString()}` : '';
    return request(`/investigations${qs}`);
  },
  getInvestigation: (id) => request(`/investigations/${id}`),
  createInvestigation: (payload) => request('/investigations', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),
  addVersion: (id, payload) => request(`/investigations/${id}/versions`, {
    method: 'POST',
    body: JSON.stringify(payload),
  }),
  deleteInvestigation: (id) => request(`/investigations/${id}`, {
    method: 'DELETE',
  }),

  // Demos
  getDemos: () => request('/demos'),
  getDemo: (demoId) => request(`/demos/${demoId}`),
  seedDemos: () => request('/demos/seed', { method: 'POST' }),

  // Claims & Mutation Analysis
  getClaimDNA: (text) => request('/claims/dna', {
    method: 'POST',
    body: JSON.stringify({ text }),
  }),
  compareClaims: (original_text, modified_text) => request('/claims/compare', {
    method: 'POST',
    body: JSON.stringify({ original_text, modified_text }),
  }),
  getClaimFamily: (versionId) => request(`/claims/family/${versionId}`),

  // System
  getHealth: () => request('/health'),
};
