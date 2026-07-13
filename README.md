# 화학 평형 시뮬레이터 v3

Streamlit으로 만든 교육용 화학 평형 실험 시뮬레이터입니다.

## 포함된 실험

1. 이산화질소 ↔ 사산화이질소  
   `2NO₂(g) ⇌ N₂O₄(g)`

2. 다이크로메이트 ↔ 크로메이트  
   `Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq)`

## v3 수정 내용

- 화면 좌측/중앙/우측 배치가 깨지지 않도록 전체 레이아웃을 다시 구성했습니다.
- 피스톤, 실린더, 분자 애니메이션을 하나의 중앙 실험 화면 안에 통합했습니다.
- SVG 조각이 텍스트로 노출되던 문제를 피하기 위해 중앙 시각화는 `components.html()`로 렌더링합니다.
- Plotly를 제거하고 Streamlit 기본 그래프 기능을 사용합니다.
- 조건을 바꿀 때마다 Q, K, 정반응 속도, 역반응 속도 그래프가 즉시 갱신됩니다.
- 조건 변화 기록을 누적하는 그래프 옵션을 추가했습니다.

## 로컬 실행

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Streamlit Cloud 배포

GitHub 저장소의 가장 바깥쪽에 아래 파일들이 있어야 합니다.

```text
streamlit_app.py
requirements.txt
README.md
.streamlit/config.toml
```

Streamlit Cloud에서 저장소와 `streamlit_app.py`를 선택해 배포하면 됩니다.

## 주의

이 앱은 실제 실험값을 정밀하게 재현하는 목적이 아니라, 르샤틀리에 원리와 Q-K 비교를 시각적으로 이해하기 위한 교육용 시뮬레이터입니다.
