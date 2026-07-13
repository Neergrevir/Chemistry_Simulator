# 화학 평형 시뮬레이터

Streamlit으로 만든 교육용 화학 평형 실험 시뮬레이터입니다.

## 포함된 실험

1. 이산화질소 ↔ 사산화이질소
   - `2NO₂(g) ⇌ N₂O₄(g)`
   - 농도, 압력, 온도 변화
   - 적갈색/무색 색 변화
   - 분자 운동 애니메이션

2. 다이크로메이트 ↔ 크로메이트
   - `Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)`
   - HCl, NaOH, H₂O 추가
   - 주황색/노란색 색 변화

## 가장 쉬운 실행 방법

### Windows

압축을 푼 뒤 `run_windows.bat` 파일을 더블클릭하세요.

### Mac / Linux

터미널에서 다음을 실행하세요.

```bash
chmod +x run_mac_linux.sh
./run_mac_linux.sh
```

## 터미널로 직접 실행하기

압축을 풀고, `streamlit_app.py`가 있는 폴더에서 아래 명령어를 실행하세요.

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Mac에서는 `python` 대신 `python3`를 써야 할 수 있습니다.

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run streamlit_app.py
```

## 자주 나는 오류

### `streamlit`은 내부 또는 외부 명령이 아닙니다

아래처럼 실행하세요.

```bash
python -m streamlit run streamlit_app.py
```

### `ModuleNotFoundError: No module named 'streamlit'`

라이브러리가 설치되지 않은 상태입니다.

```bash
python -m pip install -r requirements.txt
```

### `File does not exist: streamlit_app.py`

터미널 위치가 잘못된 것입니다. `streamlit_app.py`가 있는 폴더로 이동한 뒤 실행하세요.

## Streamlit Cloud 배포

GitHub 저장소에 다음 파일을 올리세요.

- `streamlit_app.py`
- `requirements.txt`
- `README.md`

Streamlit Community Cloud에서 Main file path를 다음으로 설정하세요.

```text
streamlit_app.py
```

## 주의

이 앱은 교육용 단순화 모델입니다. 실제 실험의 정량값은 온도, 용매, 이온세기, 농도 범위에 따라 달라질 수 있습니다.


## 오류 수정 안내

이 버전은 Streamlit Cloud에서 `ModuleNotFoundError: plotly`가 발생하지 않도록 Plotly 의존성을 제거하고 `st.line_chart`를 사용합니다. GitHub에는 `streamlit_app.py`와 `requirements.txt`를 반드시 같은 저장소 루트에 올려주세요.
