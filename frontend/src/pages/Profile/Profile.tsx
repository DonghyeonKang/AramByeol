import { useAuth } from '@/contexts/AuthContext';
import { Card } from '../../components/molecules/Card/Card';
import './Profile.css';

export const Profile = () => {
  const { user } = useAuth();

  return (
    <div className="profile-page">
      <main className="main-content">
        <section className="hero-section">
          <h1>프로필</h1>
          <p>사용자 정보 관리</p>
        </section>
        <section className="profile-section">
          <Card className="profile-card">
            <div className="profile-header">
              <span className="material-icons profile-icon">account_circle</span>
              <h2>기본 정보</h2>
            </div>
            <div className="profile-info">
              <div className="info-group">
                <label>이름</label>
                <p>{user?.name}</p>
              </div>
              <div className="info-group">
                <label>이메일</label>
                <p>{user?.email}</p>
              </div>
              <div className="info-group">
                <label>학번</label>
                <p>{user?.studentId}</p>
              </div>
            </div>
          </Card>
        </section>
      </main>
    </div>
  );
}; 