import { useAuth } from '@/contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import './UserMenu.css';

interface UserMenuProps {
  isOpen: boolean;
  onClose: () => void;
}

export const UserMenu = ({ isOpen, onClose }: UserMenuProps) => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  if (!isOpen || !user) return null;

  const handleNavigation = (path: string) => {
    navigate(path);
    onClose();
  };

  const handleLogout = () => {
    logout();
    onClose();
  };

  return (
    <div className="user-menu">
      <div className="menu-items">
        <button className="menu-item" onClick={() => handleNavigation('/profile')}>
          <span className="material-icons">person</span>
          <span>프로필</span>
        </button>
        <button className="menu-item" onClick={() => handleNavigation('/settings')}>
          <span className="material-icons">settings</span>
          <span>설정</span>
        </button>
        <div className="menu-divider"></div>
        <button className="menu-item logout" onClick={handleLogout}>
          <span className="material-icons">logout</span>
          <span>로그아웃</span>
        </button>
      </div>
    </div>
  );
}; 