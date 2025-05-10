import './Chat.css';

export const Chat = () => {
  return (
    <div className="chat-page">
      <section className="hero-section">
        <h1>채팅</h1>
        <p>기숙사 학생들과 함께 대화를 나누세요</p>
      </section>
      <main className="main-content">
        <div className="chat-section">
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