FROM ubuntu:22.04

# 기본 도구 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    gcc \
    g++ \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev \
    gobject-introspection \
    gir1.2-gtk-3.0 \
    libglib2.0-dev \
    cmake \
    meson \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# 소스 복사
COPY . .

# 로그 디렉토리 생성
RUN mkdir -p /app/log && touch /app/log/arambyeol_error.log

# 포트 개방
EXPOSE 80

# 앱 실행
CMD ["python3", "app.py"]
