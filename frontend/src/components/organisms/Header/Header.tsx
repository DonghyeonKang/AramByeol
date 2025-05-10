import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTheme } from '../../../contexts/ThemeContext';
import { Button } from '../../atoms/Button/Button';
import { NotificationList } from '../../molecules/NotificationList/NotificationList';
import logo from '@/assets/logo.png';
import { useAuth } from '@/contexts/AuthContext';
import { UserMenu } from '../../molecules/UserMenu/UserMenu';
import './Header.css';

export const Header = () => {
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [notifications, setNotifications] = useState([
    {
      id: '1',
      message: '오늘의 점심 메뉴가 업데이트되었습니다.',
      date: '방금 전',
      isRead: false,
    },
    {
      id: '2',
      message: '이번 주 식단이 업데이트되었습니다.',
      date: '1시간 전',
      isRead: false,
    },
  ]);

  const handleMarkAsRead = (id: string) => {
    setNotifications(notifications.map(notification => 
      notification.id === id 
        ? { ...notification, isRead: true }
        : notification
    ));
  };

  const handleMarkAllAsRead = () => {
    setNotifications(notifications.map(notification => ({
      ...notification,
      isRead: true
    })));
    setIsNotificationsOpen(false);
  };

  return (
    <header className="header">
      <div className="header-container">
        <h1 className="logo">
          <Link to="/">
            <img src={logo} alt="아람별" className="logo-image" />
          </Link>
        </h1>
        <nav className="nav-menu">
          <ul>
            <li><Link to="/">오늘의 식단</Link></li>
            <li><Link to="/weekly">주간 식단</Link></li>
            <li><Link to="/reviews">내 후기</Link></li>
            <li><Link to="/roommate">룸메찾기</Link></li>
            <li><Link to="/chat">채팅</Link></li>
          </ul>
        </nav>
        <div className="header-actions">
          <Button 
            variant="icon"
            size="medium"
            onClick={toggleTheme}
            className="theme-button"
          >
            <span className="material-icons">
              {theme === 'light' ? 'dark_mode' : 'light_mode'}
            </span>
          </Button>
          <div className="notification-wrapper">
            <Button 
              variant="icon"
              size="medium"
              onClick={() => setIsNotificationsOpen(!isNotificationsOpen)}
              className="notification-button"
            >
              <span className="material-icons">
                {notifications.some(n => !n.isRead) ? 'notifications_active' : 'notifications'}
              </span>
              {notifications.some(n => !n.isRead) && (
                <span className="notification-badge" />
              )}
            </Button>
            <NotificationList
              notifications={notifications}
              isOpen={isNotificationsOpen}
              onClose={() => setIsNotificationsOpen(false)}
              onMarkAsRead={handleMarkAsRead}
              onMarkAllAsRead={handleMarkAllAsRead}
            />
          </div>
          {user ? (
            <div className="user-menu-wrapper">
              <Button 
                variant="icon"
                size="medium"
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="auth-button"
              >
                <span className="material-icons">account_circle</span>
              </Button>
              <UserMenu 
                isOpen={isUserMenuOpen}
                onClose={() => setIsUserMenuOpen(false)}
              />
            </div>
          ) : (
            <Button 
              variant="icon"
              size="medium"
              onClick={() => navigate('/login')}
              className="auth-button"
            >
              <span className="material-icons">login</span>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};