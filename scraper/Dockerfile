FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

# 타임존 설정
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 로그 디렉토리 생성
RUN mkdir -p /app/logs
VOLUME /app/logs

# html_files 디렉토리 생성
RUN mkdir -p /app/html_files
VOLUME /app/html_files

CMD ["python", "scheduler.py"]