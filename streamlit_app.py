
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Matplotlib에서 한글 폰트가 깨지지 않도록 설정 (Windows 기준)
# macOS는 'AppleGothic', Linux는 'NanumGothic' 등을 시도해볼 수 있습니다.
try:
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
except:
    print("한글 폰트를 찾을 수 없어 기본 폰트로 설정됩니다.")
    pass

# 특수각에 대한 루트/분수 표현을 딕셔너리로 정의
special_angles = {
    0:   ("0", "1", "0"),
    30:  ("1/2", "√3/2", "√3/3"),
    45:  ("√2/2", "√2/2", "1"),
    60:  ("√3/2", "1/2", "√3"),
    90:  ("1", "0", "정의되지 않음"),
    120: ("√3/2", "-1/2", "-√3"),
    135: ("√2/2", "-√2/2", "-1"),
    150: ("1/2", "-√3/2", "-√3/3"),
    180: ("0", "-1", "0"),
    210: ("-1/2", "-√3/2", "√3/3"),
    225: ("-√2/2", "-√2/2", "1"),
    240: ("-√3/2", "-1/2", "√3"),
    270: ("-1", "0", "정의되지 않음"),
    300: ("-√3/2", "1/2", "-√3"),
    315: ("-√2/2", "√2/2", "-1"),
    330: ("-1/2", "√3/2", "-√3/3"),
    360: ("0", "1", "0"),
}


def draw_unit_circle(ax, angle_rad, sin_val, cos_val):
    """단위원과 각도에 따른 삼각형을 그리는 함수"""
    
    # 1. 단위원, x/y축, 그리드 그리기
    circle = patches.Circle((0, 0), radius=1, fill=False, color='black', linewidth=1.5)
    ax.add_patch(circle)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.6)

    # 2. 반지름(빗변), cos, sin 선분 그리기
    ax.plot([0, cos_val], [0, sin_val], 'r-', linewidth=2, label='반지름 (r=1)')
    ax.plot([0, cos_val], [0, 0], 'b-', linewidth=2, label=f'cos(θ) = {cos_val:.2f}')
    ax.plot([cos_val, cos_val], [0, sin_val], 'g-', linewidth=2, label=f'sin(θ) = {sin_val:.2f}')
    
    # 3. 각도(호) 표시
    angle_deg = np.degrees(angle_rad)
    arc = patches.Arc((0, 0), 0.4, 0.4, angle=0, theta1=0, theta2=angle_deg, color='purple', linewidth=1.5)
    ax.add_patch(arc)
    ax.text(0.25 * np.cos(angle_rad / 2), 0.25 * np.sin(angle_rad / 2), f'θ', fontsize=12, color='purple')

    # 4. 원 위의 점 표시
    ax.plot(cos_val, sin_val, 'ro', label='(cosθ, sinθ)')

    # 5. 그래프 설정
    ax.set_title("단위원 시각화", fontsize=15)
    ax.legend(loc='upper right')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("cos(θ) [x 좌표]")
    ax.set_ylabel("sin(θ) [y 좌표]")


def draw_trig_functions(ax, angle_rad, sin_val, cos_val, tan_val):
    """삼각함수 그래프와 현재 각도 위치를 그리는 함수"""
    x = np.linspace(0, 2 * np.pi, 400)
    
    # 1. sin, cos, tan 그래프 그리기
    ax.plot(x, np.sin(x), label='sin(x)', color='g')
    ax.plot(x, np.cos(x), label='cos(x)', color='b')
    ax.plot(x, np.tan(x), label='tan(x)', color='orange', linestyle='--')

    # 2. 현재 각도 위치에 점 표시
    ax.plot(angle_rad, sin_val, 'go', markersize=8)
    ax.plot(angle_rad, cos_val, 'bo', markersize=8)
    # tan값이 너무 크거나 작으면 점이 보이지 않으므로 y축 범위 내에 있을 때만 표시
    if tan_val is not None and -4 < tan_val < 4:
        ax.plot(angle_rad, tan_val, 'o', color='orange', markersize=8)

    # 3. 그래프 설정
    ax.set_title("삼각함수 그래프", fontsize=15)
    ax.set_xlabel("각도 (Radian)")
    ax.set_ylabel("값")
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    ax.set_ylim(-2, 2) # tan 그래프가 무한대로 뻗어나가지 않게 y축 범위 제한
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')


# --- Streamlit 앱 메인 UI ---

st.set_page_config(layout="wide") # 넓은 화면 레이아웃 사용

st.title("✨ 삼각함수 시각화 애플리케이션")
st.write("학생들이 각도(θ)에 따라 사인, 코사인, 탄젠트 값이 어떻게 변하는지 직관적으로 이해할 수 있도록 돕는 도구입니다.")

# 사이드바에 슬라이더 배치
st.sidebar.header("👇 각도(θ)를 조절하세요")
angle_deg = st.sidebar.slider("각도 (Degrees)", min_value=0, max_value=360, value=45, step=1)

# 각도 계산
angle_rad = np.radians(angle_deg)
sin_val = np.sin(angle_rad)
cos_val = np.cos(angle_rad)
tan_val = np.tan(angle_rad) if not np.isclose(np.cos(angle_rad), 0) else None

# 특수각인지 확인하고 표시할 문자열 결정
if angle_deg in special_angles:
    sin_str, cos_str, tan_str = special_angles[angle_deg]
else:
    sin_str = f"{sin_val:.4f}"
    cos_str = f"{cos_val:.4f}"
    tan_str = f"{tan_val:.4f}" if tan_val is not None else "정의되지 않음"

# 계산 결과 표시
st.header(f"선택된 각도: {angle_deg}°")

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Radian", value=f"{angle_rad:.4f}")
col2.metric(label="Sin(θ)", value=sin_str)
col3.metric(label="Cos(θ)", value=cos_str)
col4.metric(label="Tan(θ)", value=tan_str)

st.markdown("---")

# 시각화 자료 표시
st.header("시각화 자료")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

draw_unit_circle(ax1, angle_rad, sin_val, cos_val)
draw_trig_functions(ax2, angle_rad, sin_val, cos_val, tan_val)

st.pyplot(fig)

# 학습 가이드 (펼치기/접기 기능)
with st.expander("📝 학습 가이드 보기"):
    st.markdown("""
    #### 단위원 (왼쪽 그래프)
    - 반지름이 1인 원을 **단위원**이라고 합니다.
    - 원 위의 한 점의 **x좌표가 `cos(θ)` 값**이고, **y좌표가 `sin(θ)` 값**입니다.
    - 슬라이더를 움직이며 각도(θ)가 변할 때, 파란색 선(`cos`)과 초록색 선(`sin`)의 길이가 어떻게 변하는지 관찰해보세요.
    - 0°, 90°, 180°, 270° 등 축에 각도가 위치할 때 `sin`과 `cos` 값이 어떻게 1, 0, -1이 되는지 확인해보세요.

    #### 삼각함수 그래프 (오른쪽 그래프)
    - 이 그래프는 각도(x축)에 따른 `sin`, `cos`, `tan`의 변화를 전체적으로 보여줍니다.
    - 슬라이더를 움직이면 현재 각도에 해당하는 위치에 **큰 점**이 표시됩니다.
    - 단위원에서 `sin` 값이 최대가 되는 90°에서, `sin` 그래프가 가장 높은 지점(1)에 도달하는 것을 볼 수 있습니다.
    - `tan` 함수는 `cos(θ)`가 0이 되는 90°(π/2)와 270°(3π/2)에서 값이 무한대로 가기 때문에 **점근선**을 가집니다.

    #### 특수각
    - 슬라이더로 30°, 45°, 60° 등 **특수각**을 선택하면, 값이 소수점이 아닌 **루트(√)와 분수**로 표현됩니다. 이를 통해 학생들이 암기한 값과 일치하는지 쉽게 확인할 수 있습니다.
    """)
