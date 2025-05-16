import { Card } from '../../molecules/Card/Card';
import './ReviewModal.css';

interface ReviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  menuName: string;
  score: number;
  reviewCount: number;
}

export const ReviewModal = ({ isOpen, onClose, menuName, score, reviewCount }: ReviewModalProps) => {
  if (!isOpen) return null;

  // 목업 리뷰 데이터
  const mockReviews = [
    { id: 1, author: "익명", content: "맛있어요!", score: 5, date: "2024-03-15" },
    { id: 2, author: "익명", content: "평범해요", score: 3, date: "2024-03-14" },
    { id: 3, author: "익명", content: "괜찮았습니다", score: 4, date: "2024-03-13" },
  ];

  // 목업 평점 분포 데이터
  const ratingDistribution = [
    { score: 5, count: 15 },
    { score: 4, count: 5 },
    { score: 3, count: 2 },
    { score: 2, count: 1 },
    { score: 1, count: 0 },
  ];

  const maxCount = Math.max(...ratingDistribution.map(r => r.count));

  // 목업 시간별 트렌드 데이터 (최근 6개월)
  const trendData = [
    { month: '10월', score: 3.5 },
    { month: '11월', score: 3.8 },
    { month: '12월', score: 4.0 },
    { month: '1월', score: 4.2 },
    { month: '2월', score: 4.3 },
    { month: '3월', score: 4.5 },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <Card 
        className="review-modal" 
        onClick={(e: React.MouseEvent) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h3>{menuName}</h3>
          <button className="close-button" onClick={onClose}>
            <span className="material-icons">close</span>
          </button>
        </div>
        <div className="menu-rating">
          <div className="rating-score">
            <span className="material-icons">star</span>
            <span>{score}</span>
          </div>
          <span className="rating-count">{reviewCount}개의 평가</span>
        </div>
        <div className="trend-section">
          <h4>평점 트렌드</h4>
          <div className="trend-graph">
            <div className="trend-lines">
              {trendData.map((data, index) => {
                const nextScore = trendData[index + 1]?.score;
                if (nextScore) {
                  const x1 = `${(index * 20)}%`;
                  const x2 = `${((index + 1) * 20)}%`;
                  const y1 = `${100 - (data.score * 20)}%`;
                  const y2 = `${100 - (nextScore * 20)}%`;
                  
                  return (
                    <svg key={index} className="trend-line">
                      <line
                        x1={x1}
                        y1={y1}
                        x2={x2}
                        y2={y2}
                        stroke="#ffd700"
                        strokeWidth="2"
                      />
                    </svg>
                  );
                }
                return null;
              })}
            </div>
            <div className="trend-points">
              {trendData.map((data, index) => (
                <div
                  key={index}
                  className="trend-point"
                  style={{
                    left: `${index * 20}%`,
                    bottom: `${(data.score * 20) - 10}%`
                  }}
                  title={`${data.month}: ${data.score.toFixed(1)}점`}
                >
                  <div className="point"></div>
                  <div className="point-label">{data.month}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="rating-distribution">
          {ratingDistribution.map((rating) => (
            <div key={rating.score} className="rating-bar">
              <span className="rating-label">{rating.score}점</span>
              <div className="bar-container">
                <div 
                  className="bar" 
                  style={{ 
                    width: `${(rating.count / maxCount) * 100}%`,
                    opacity: rating.count === 0 ? 0.3 : 1
                  }}
                />
              </div>
              <span className="rating-count-label">{rating.count}</span>
            </div>
          ))}
        </div>
        <div className="reviews-list">
          {mockReviews.map(review => (
            <div key={review.id} className="review-item">
              <div className="review-header">
                <div className="review-author">{review.author}</div>
                <div className="review-score">
                  <span className="material-icons">star</span>
                  <span>{review.score}</span>
                </div>
              </div>
              <p className="review-content">{review.content}</p>
              <div className="review-date">{review.date}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}; 