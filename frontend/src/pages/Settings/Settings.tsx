import { useTheme } from '@/contexts/ThemeContext';
import { Card } from '../../components/molecules/Card/Card';
import './Settings.css';

export const Settings = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="settings-page">
      <main className="main-content">
        <section className="hero-section">
          <h1>설정</h1>
          <p>앱 설정 관리</p>
        </section>
        <section className="settings-section">
          <Card className="settings-card">
            <div className="settings-header">
              <span className="material-icons settings-icon">settings</span>
              <h2>앱 설정</h2>
            </div>
            <div className="settings-options">
              <div className="setting-item">
                <div className="setting-info">
                  <h3>다크 모드</h3>
                  <p>화면 테마를 변경합니다</p>
                </div>
                <button className="theme-toggle" onClick={toggleTheme}>
                  <span className="material-icons">
                    {theme === 'light' ? 'dark_mode' : 'light_mode'}
                  </span>
                  {theme === 'light' ? '다크 모드' : '라이트 모드'}
                </button>
              </div>
            </div>
          </Card>
        </section>
      </main>
    </div>
  );
}; 