export type Theme = 'light' | 'dark';

export interface User {
  id: string;
  username: string;
  email: string;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
} 