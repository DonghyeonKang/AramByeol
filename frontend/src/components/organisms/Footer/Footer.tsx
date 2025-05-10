import './Footer.css';

export const Footer = () => {
  const schedules = [
    {
      title: '평일',
      times: [
        { meal: '아침', time: '07:30 - 09:00' },
        { meal: 'Take Out', time: '08:30 - 09:30' },
        { meal: '점심', time: '11:30 - 13:30' },
        { meal: '저녁', time: '17:30 - 19:00' },
      ],
    },
    {
      title: '주말',
      times: [
        { meal: '아침', time: '08:00 - 09:00' },
        { meal: '점심', time: '12:00 - 13:30' },
        { meal: '저녁', time: '17:30 - 18:40' },
      ],
    },
    {
      title: '방학 평일',
      times: [
        { meal: '아침', time: '08:00 - 09:00' },
        { meal: 'Take Out', time: '08:30 - 09:30' },
        { meal: '점심', time: '12:00 - 13:30' },
        { meal: '저녁', time: '17:30 - 18:30' },
      ],
    },
    {
      title: '방학 주말',
      times: [
        { meal: '아침', time: '08:00 - 09:00' },
        { meal: '점심', time: '12:00 - 13:30' },
        { meal: '저녁', time: '17:30 - 18:30' },
      ],
    },
  ];

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-left">
            <div className="footer-section">
              <h4>아람별 소개</h4>
              <p>경상국립대학교 학생들을 위한</p>
              <p>식단 정보 서비스입니다.</p>
            </div>
            <div className="footer-section">
              <h4>연락처</h4>
              <p>경상국립대학교 가좌캠퍼스</p>
              <p>경남 진주시 진주대로 501</p>
            </div>
          </div>
          <div className="schedule-section">
            <h3>식당 운영 시간</h3>
            <div className="schedules">
              {schedules.map((schedule) => (
                <div key={schedule.title} className="schedule-group">
                  <h4>{schedule.title}</h4>
                  <ul>
                    {schedule.times.map((time) => (
                      <li key={time.meal}>
                        <span>{time.meal}</span>
                        <span>{time.time}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2024 아람별. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}; 