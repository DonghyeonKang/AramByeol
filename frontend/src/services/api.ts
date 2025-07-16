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
  },

  async sendVerification(email: string) {
    const response = await fetch(`${BASE_URL}/api/auth/send-verification`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    if (!response.ok) throw new Error('인증 메일 발송 실패');
    return response;
  },

  async verifyCode(email: string, code: string) {
    const response = await fetch(`${BASE_URL}/api/auth/verify-code`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, code }),
    });
    if (!response.ok) throw new Error('인증번호 확인 실패');
    return response.json(); // true/false 반환
  }
}; 