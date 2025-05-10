import './Roommate.css';

export const Roommate = () => {
  return (
    <div className="roommate-page">
      <section className="hero-section">
        <h1>룸메이트</h1>
        <p>학기를 함께 할 룸메이트를 찾아보세요</p>
      </section>
      <main className="main-content">
        <div className="roommate-section">
          <div className="coming-soon">
            <span className="material-icons">engineering</span>
            <h2>준비 중인 서비스입니다</h2>
            <p>더 나은 서비스로 찾아뵙겠습니다</p>
          </div>
        </div>
      </main>
    </div>
  );
}; 