import './Reviews.css';

export const Reviews = () => {
  return (
    <div className="reviews-page">
      <section className="hero-section">
        <h1>내 후기</h1>
        <p>나의 식사 후기를 관리하세요</p>
      </section>
      <main className="main-content">
        <div className="reviews-section">
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