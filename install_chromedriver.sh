#!/bin/bash
set -e

# Chrome 버전 확인
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
echo "[INFO] Chrome 버전: $CHROME_VERSION"

# ChromeDriver 다운로드 URL 구성
CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip"

# ChromeDriver 다운로드 및 설치
wget -q "$CHROMEDRIVER_URL" -O chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver_linux64.zip chromedriver-linux64

echo "[INFO] ChromeDriver 설치 완료!"
