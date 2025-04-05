FROM ubuntu:22.04

# 시스템 패키지 및 크롬 의존성 설치
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    gcc g++ build-essential \
    pkg-config \
    libcairo2-dev libgirepository1.0-dev gobject-introspection gir1.2-gtk-3.0 \
    libglib2.0-dev \
    cmake meson \
    wget curl unzip gnupg ca-certificates \
    fonts-liberation \
    libappindicator3-1 libatk-bridge2.0-0 libgtk-3-0 libnss3 libxss1 libasound2 \
    libxshmfence-dev libxrandr2 libgbm-dev libu2f-udev libvulkan1 xdg-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Google Chrome 설치
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# ChromeDriver 설치 스크립트 복사 및 실행
COPY install_chromedriver.sh /tmp/install_chromedriver.sh
RUN chmod +x /tmp/install_chromedriver.sh && /tmp/install_chromedriver.sh

# 환경 변수 설정
ENV CHROME_BIN=/usr/bin/google-chrome
ENV PATH=$PATH:/usr/local/bin

# 작업 디렉토리 설정
WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# 소스 코드 복사
COPY . .

# 로그 디렉토리 생성
RUN mkdir -p /app/log && touch /app/log/arambyeol_error.log

EXPOSE 80
CMD ["python3", "app.py"]
