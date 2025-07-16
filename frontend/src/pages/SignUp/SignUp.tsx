import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../../components/atoms/Input/Input';
import { Button } from '../../components/atoms/Button/Button';
import { Card } from '../../components/molecules/Card/Card';
import './SignUp.css';
import { api } from '@/services/api';

interface SignUpForm {
  email: string;
  password: string;
  passwordConfirm: string;
  name: string;
  studentId: string;
  verificationCode: string;
}

export const SignUp = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<SignUpForm>({
    email: '',
    password: '',
    passwordConfirm: '',
    name: '',
    studentId: '',
    verificationCode: '',
  });
  const [error, setError] = useState('');
  const [isEmailSent, setIsEmailSent] = useState(false);
  const [isEmailVerified, setIsEmailVerified] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [timer, setTimer] = useState(0); // 남은 시간(초)
  const [timerId, setTimerId] = useState<NodeJS.Timeout | null>(null);

  // 타이머 시작 함수
  const startTimer = () => {
    if (timerId) clearInterval(timerId);
    setTimer(300); // 5분(300초)
    const id = setInterval(() => {
      setTimer(prev => {
        if (prev <= 1) {
          clearInterval(id);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    setTimerId(id);
  };

  // 언마운트 시 타이머 정리
  useEffect(() => {
    return () => {
      if (timerId) clearInterval(timerId);
    };
  }, [timerId]);

  const handleSendVerification = async () => {
    if (!formData.email.endsWith('@gnu.ac.kr')) {
      setError('경상국립대학교 이메일(@gnu.ac.kr)만 사용 가능합니다.');
      return;
    }

    setIsLoading(true);
    try {
      await api.sendVerification(formData.email);
      setIsEmailSent(true);
      setError('');
      startTimer(); // 타이머 시작
    } catch (err) {
      setError('인증 메일 발송 중 오류가 발생했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyCode = async () => {
    setIsLoading(true);
    try {
      const result = await api.verifyCode(formData.email, formData.verificationCode);
      if (result === true) {
        setIsEmailVerified(true);
        setError('');
        if (timerId) clearInterval(timerId);
      } else {
        setError('인증번호가 올바르지 않습니다.');
      }
    } catch (err) {
      setError('인증번호 확인 중 오류가 발생했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!isEmailVerified) {
      setError('이메일 인증이 필요합니다.');
      return;
    }

    if (formData.password !== formData.passwordConfirm) {
      setError('비밀번호가 일치하지 않습니다.');
      return;
    }

    try {
      const response = await fetch('/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          name: formData.name,
          studentId: formData.studentId,
        }),
      });

      if (!response.ok) {
        throw new Error('회원가입에 실패했습니다.');
      }

      navigate('/login');
    } catch (err) {
      setError('회원가입 중 오류가 발생했습니다.');
    }
  };

  return (
    <div className="signup-page">
      <main className="signup-content">
        <Card className="signup-card">
          <h2>회원가입</h2>
          {error && <p className="error-message">{error}</p>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <div className="email-verification-group">
                <Input
                  type="email"
                  label="학교 이메일"
                  placeholder="example@gnu.ac.kr"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  disabled={isEmailVerified}
                  required
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleSendVerification}
                  disabled={isEmailVerified || isLoading}
                >
                  {isEmailSent ? '재전송' : '인증번호 전송'}
                </Button>
              </div>
            </div>

            {isEmailSent && !isEmailVerified && (
              <div className="form-group">
                <div className="email-verification-group">
                  <Input
                    type="text"
                    label="인증번호"
                    value={formData.verificationCode}
                    onChange={(e) => setFormData({ ...formData, verificationCode: e.target.value })}
                    required
                    disabled={timer === 0}
                  />
                  <Button
                    type="button"
                    onClick={handleVerifyCode}
                    disabled={isLoading || timer === 0}
                  >
                    확인
                  </Button>
                  <span className="timer">
                    {timer > 0
                      ? `남은 시간: ${Math.floor(timer / 60)}:${(timer % 60).toString().padStart(2, '0')}`
                      : '인증번호가 만료되었습니다'}
                  </span>
                </div>
              </div>
            )}

            {isEmailVerified && (
              <>
                <div className="form-group">
                  <Input
                    type="password"
                    label="비밀번호"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <Input
                    type="password"
                    label="비밀번호 확인"
                    value={formData.passwordConfirm}
                    onChange={(e) => setFormData({ ...formData, passwordConfirm: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <Input
                    type="text"
                    label="이름"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <Input
                    type="text"
                    label="학번"
                    value={formData.studentId}
                    onChange={(e) => setFormData({ ...formData, studentId: e.target.value })}
                    required
                  />
                </div>
                <Button type="submit" className="signup-button" disabled={isLoading}>
                  회원가입
                </Button>
              </>
            )}
          </form>
          <div className="signup-footer">
            <p>이미 계정이 있으신가요? <a href="/login">로그인</a></p>
          </div>
        </Card>
      </main>
    </div>
  );
}; 