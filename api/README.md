# 아람별 (Arambyeol) 프로젝트

## 개발 환경
- Java 17
- Spring Boot 3.2.3
- Gradle
- MySQL 8.0 (Production)
- H2 Database (Local Development)

## API 문서 (Swagger UI)
- Local 환경: http://localhost:8080/swagger-ui.html
- Production 환경: http://your-production-url/swagger-ui.html

### Swagger 관련 엔드포인트
- Swagger UI: `/swagger-ui.html`
- API 문서: `/v3/api-docs`
- API 문서 (YAML 형식): `/v3/api-docs.yaml`

## 데이터베이스 접속 정보

### Local 환경 (H2 Database)
- Console URL: http://localhost:8080/h2-console
- JDBC URL: `jdbc:h2:mem:arambyeol`
- Username: `sa`
- Password: (empty)

### Production 환경 (MySQL)
- Host: `mysql:3306`
- Database: `arambyeol`
- Username: `root`
- Password: `root`

## 프로젝트 실행 방법

### Local 환경
```bash
./gradlew bootRun
```

### Docker 환경
```bash
docker-compose up --build
```

## API 엔드포인트

### 사용자 관리
- 회원가입: `POST /users/register`
- 로그인: `POST /users/login`
- 사용자명 중복 확인: `GET /users/check/{username}`
- 비밀번호 재설정: `POST /users/password/reset`

### 조회수 관리
- 조회수 확인: `GET /views/{id}`
- 조회수 증가: `POST /views/{id}/increment`

## 데이터베이스 스키마

### 테이블 구조
- users: 사용자 정보
  - user_id (PK)
  - username (Unique)
  - password
  - created_at
  - updated_at

- menu: 메뉴 정보
  - menu_id (PK)
  - menu (Unique)
  - img_path

- plan: 식단 계획
  - plan_id (PK)
  - menu_id (FK)
  - course
  - date

- review: 메뉴 리뷰
  - review_id (PK)
  - user_id (FK)
  - menu_id (FK)
  - score

- views: 조회수 관리
  - id (PK)
  - views

## 보안 설정
- 모든 API 엔드포인트는 `/api/**` 경로로 시작
- Swagger UI와 H2 Console은 개발 환경에서만 접근 가능
- Production 환경에서는 적절한 보안 설정 필요

## 문제 해결

### H2 Console 접속 불가 시
1. application.yml의 `spring.h2.console.enabled` 설정이 `true`인지 확인
2. SecurityConfig에서 H2 Console 경로가 허용되어 있는지 확인
3. 올바른 JDBC URL을 사용하고 있는지 확인

### Swagger UI 접속 불가 시
1. build.gradle에 springdoc-openapi 의존성이 포함되어 있는지 확인
2. SecurityConfig에서 Swagger UI 관련 경로가 허용되어 있는지 확인
3. application.yml의 springdoc 설정이 올바른지 확인

## 참고 사항
- Local 환경에서는 H2 인메모리 데이터베이스를 사용하므로 애플리케이션 재시작 시 데이터가 초기화됨
- Production 환경에서는 MySQL을 사용하며, 데이터가 영구 저장됨
- API 문서는 Swagger UI를 통해 실시간으로 확인 가능 