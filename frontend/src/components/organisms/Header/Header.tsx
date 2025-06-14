import { useState, useEffect, useRef } from 'react';
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
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isMenuVisible, setIsMenuVisible] = useState(false);
  const [isMobileSmall, setIsMobileSmall] = useState(false);
  const [isPc, setIsPc] = useState(true);
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const { user } = useAuth();
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
  const menuTimeout = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const handleResize = () => {
      setIsMobileSmall(window.innerWidth <= 768);
      setIsPc(window.innerWidth > 1024);
    };
    handleResize(); // 초기 체크
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

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

  const handleMenuToggle = () => {
    if (!isMenuOpen) {
      setIsMenuVisible(true);
      setTimeout(() => setIsMenuOpen(true), 10); // 트랜지션 시작
    } else {
      setIsMenuOpen(false);
      if (menuTimeout.current) clearTimeout(menuTimeout.current);
      menuTimeout.current = setTimeout(() => setIsMenuVisible(false), 300); // 트랜지션 후 제거
    }
  };

  return (
    <header className="header">
      <div className="header-container">
        <h1 className="logo">
          <Link to="/">
            <img src={logo} alt="아람별" className="logo-image" />
          </Link>
        </h1>
        {isPc ? (
          <nav className="nav-menu">
            <ul>
              <li><Link to="/">오늘의 식단</Link></li>
              <li><Link to="/weekly">주간 식단</Link></li>
              <li><Link to="/reviews">내 후기</Link></li>
              <li><Link to="/roommate">룸메이트</Link></li>
              <li><Link to="/chat">채팅</Link></li>
            </ul>
          </nav>
        ) : (
          isMenuVisible && (
            <>
              <div className="menu-overlay" onClick={handleMenuToggle} />
              <nav className={`nav-menu${isMenuOpen ? ' open' : ''}`}>
                <ul>
                  <li><Link to="/" onClick={handleMenuToggle}>오늘의 식단</Link></li>
                  <li><Link to="/weekly" onClick={handleMenuToggle}>주간 식단</Link></li>
                  <li><Link to="/reviews" onClick={handleMenuToggle}>내 후기</Link></li>
                  <li><Link to="/roommate" onClick={handleMenuToggle}>룸메이트</Link></li>
                  <li><Link to="/chat" onClick={handleMenuToggle}>채팅</Link></li>
                </ul>
              </nav>
            </>
          )
        )}
        <div className="header-actions">
          <Button 
            variant="icon"
            size={isMobileSmall ? "small" : "medium"}
            onClick={toggleTheme}
            className="theme-button button icon"
          >
            <span className="material-icons">
              {theme === 'light' ? 'dark_mode' : 'light_mode'}
            </span>
          </Button>
          <div className="notification-wrapper">
            <Button 
              variant="icon"
              size={isMobileSmall ? "small" : "medium"}
              onClick={() => setIsNotificationsOpen(!isNotificationsOpen)}
              className="notification-button button icon"
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
              onMarkAsRead={handleMarkAsRead}
              onMarkAllAsRead={handleMarkAllAsRead}
            />
          </div>
          {user ? (
            <div className="user-menu-wrapper">
              <Button 
                variant="icon"
                size={isMobileSmall ? "small" : "medium"}
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="auth-button button icon"
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
              size={isMobileSmall ? "small" : "medium"}
              onClick={() => navigate('/login')}
              className="auth-button button icon"
            >
              <span className="material-icons">login</span>
            </Button>
          )}
          {!isPc && (
            <Button
              variant="icon"
              size={isMobileSmall ? "small" : "medium"}
              className={`menu-toggle button icon${isMenuOpen ? ' open' : ''}`}
              aria-label="메뉴 열기"
              onClick={handleMenuToggle}
            >
              <span className="sr-only">메뉴 열기</span>
              <span className="icon-fade-wrap">
                <span
                  className={`material-icons icon-fade menu-icon ${isMobileSmall ? 'small' : 'medium'}${isMenuOpen ? '' : ' visible'}`}
                >
                  menu
                </span>
                <span
                  className={`material-icons icon-fade close-icon ${isMobileSmall ? 'small' : 'medium'}${isMenuOpen ? ' visible' : ''}`}
                >
                  close
                </span>
              </span>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};