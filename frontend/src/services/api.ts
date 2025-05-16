const BASE_URL = import.meta.env.VITE_API_URL;

export const api = {
  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error('API request failed');
    }
    return response.json();
  },

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('API request failed');
    }
    return response.json();
  },

  async getWeeklyPlan(date: string) {
    const response = await fetch(`${BASE_URL}/plans/weekly/${date}`);
    if (!response.ok) {
      throw new Error('Failed to fetch weekly plan');
    }
    return response.json();
  },

  async getDailyPlan(date: string) {
    const response = await fetch(`${BASE_URL}/plans/${date}`);
    if (!response.ok) {
      throw new Error('Failed to fetch daily plan');
    }
    return response.json();
  }
}; 