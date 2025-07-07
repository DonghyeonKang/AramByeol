import { createContext, useContext, useState, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
  studentId: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// 목업 사용자 데이터
const mockUser = {
  id: '1',
  email: 'test@gnu.ac.kr',
  name: '홍길동',
  studentId: '2024123456'
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    try {
      // 개발 환경에서는 목업 데이터 사용
      if (import.meta.env.DEV) {
        if (email === 'test@gnu.ac.kr' && password === 'password') {
          setUser(mockUser);
          return;
        }
        throw new Error('이메일 또는 비밀번호가 올바르지 않습니다.');
      }

      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('로그인에 실패했습니다.');
      }

      const data = await response.json();
      setUser(data.user);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 