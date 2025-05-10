import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Input } from '../../components/atoms/Input/Input';
import { Button } from '../../components/atoms/Button/Button';
import { Card } from '../../components/molecules/Card/Card';
import { useAuth } from '@/contexts/AuthContext';
import './Login.css';

export const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(formData.email, formData.password);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : '로그인에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">
      <main className="login-content">
        <Card className="login-card">
          <h2>로그인</h2>
          {error && <p className="error-message">{error}</p>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <Input
                type="email"
                label="이메일"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <Input
                type="password"
                label="비밀번호"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
              />
            </div>
            <Button 
              type="submit" 
              className="login-button"
              disabled={isLoading}
            >
              {isLoading ? '로그인 중...' : '로그인'}
            </Button>
          </form>
          <div className="login-footer">
            <p>계정이 없으신가요? <Link to="/signup">회원가입</Link></p>
          </div>
        </Card>
      </main>
    </div>
  );
}; 