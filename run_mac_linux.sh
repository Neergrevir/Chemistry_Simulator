#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "[1/2] 필요한 라이브러리를 설치합니다..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "[2/2] Streamlit 앱을 실행합니다..."
python3 -m streamlit run streamlit_app.py
