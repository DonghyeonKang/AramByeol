import './NotificationList.css';

interface Notification {
  id: string;
  message: string;
  date: string;
  isRead: boolean;
}

interface NotificationListProps {
  notifications: Notification[];
  isOpen: boolean;
  onMarkAsRead: (id: string) => void;
  onMarkAllAsRead: () => void;
}

export const NotificationList = ({ 
  notifications, 
  isOpen, 
  onMarkAsRead,
  onMarkAllAsRead 
}: NotificationListProps) => {
  if (!isOpen) return null;

  return (
    <div className="notification-list">
      <div className="notification-header">
        <h3>알림</h3>
        <button className="mark-all-read" onClick={onMarkAllAsRead}>
          <span className="material-icons">done_all</span>
          모두 읽음
        </button>
      </div>
      <div className="notification-items">
        {notifications.length > 0 ? (
          notifications.map((notification) => (
            <div 
              key={notification.id} 
              className={`notification-item ${notification.isRead ? 'read' : ''}`}
            >
              <div className="notification-content">
                <p>{notification.message}</p>
                <span className="notification-date">{notification.date}</span>
              </div>
              {!notification.isRead && (
                <button 
                  className="mark-read"
                  onClick={() => onMarkAsRead(notification.id)}
                >
                  <span className="material-icons">done</span>
                </button>
              )}
            </div>
          ))
        ) : (
          <div className="no-notifications">
            <p>새로운 알림이 없습니다</p>
          </div>
        )}
      </div>
    </div>
  );
}; 