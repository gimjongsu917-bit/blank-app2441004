
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Matplotlib에서 한글 폰트가 깨지지 않도록 설정
# (실행 환경에 따라 폰트 경로를 확인해야 할 수 있습니다.)
# Windows: 'Malgun Gothic', macOS: 'AppleGothic', Linux: 'NanumGothic' 등
try:
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
except:
    # 대체 폰트 설정 (없을 경우 기본 폰트로 표시됨)
    pass


def draw_unit_circle(ax, angle_rad, sin_val, cos_val):
    """단위원과 각도에 따른 삼각형을 그리는 함수"""
    
    # 1. 단위원 그리기
    circle = patches.Circle((0, 0), radius=1, fill=False, color='black', linewidth=1.5)
    ax.add_patch(circle)

    # 2. x, y축 그리기
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.6)

    # 3. 각도에 해당하는 반지름(빗변) 그리기
    ax.plot([0, cos_val], [0, sin_val], 'r-', linewidth=2, label='반지름 (r=1)')

    # 4. cos(θ)와 sin(θ) 선분 그리기
    # cos(θ) - x축 성분 (밑변)
    ax.plot([0, cos_val], [0, 0], 'b-', linewidth=2, label=f'cos(θ) = {cos_val:.2f}')
    # sin(θ) - y축 성분 (높이)
    ax.plot([cos_val, cos_val], [0, sin_val], 'g-', linewidth=2, label=f'sin(θ) = {sin_val:.2f}')
    
    # 5. 각도 표시
    angle_deg = np.degrees(angle_rad)
    arc = patches.Arc((0, 0), 0.4, 0.4, angle=0, theta1=0, theta2=angle_deg, color='purple', linewidth=1.5)
    ax.add_patch(arc)
    ax.text(0.25 * np.cos(angle_rad / 2), 0.25 * np.sin(angle_rad / 2), f'θ', fontsize=12, color='purple')

    # 점 표시
    ax.plot(cos_val, sin_val, 'ro') # 반지름 끝점

    ax.set_title("단위원 시각화", fontsize=15)
    ax.legend(loc='upper right')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("cos(θ)")
    ax.set_ylabel("sin(θ)")


def draw_trig_functions(ax, angle_rad, sin_val, cos_val, tan_val):
    """삼각함수 그래프와 현재 각도 위치를 그리는 함수"""
    x = np.linspace(0, 2 * np.pi, 400)
    
    # 그래프 그리기
    ax.plot(x, np.sin(x), label='sin(x)', color='g')
    ax.plot(x, np.cos(x), label='cos(x)', color='b')
    ax.plot(x, np.tan(x), label='tan(x)', color='orange', linestyle='--')

    # 현재 각도 위치에 점 찍기
    ax.plot(angle_rad, sin_val, 'go', markersize=8)
    ax.plot(angle_rad, cos_val, 'bo', markersize=8)
    if tan_val is not None:
        ax.plot(angle_rad, tan_val, 'o', color='orange', markersize=8)

    ax.set_title("삼각함수 그래프", fontsize=15)
    ax.set_xlabel("각도 (Radian)")
    ax.set_ylabel("값")
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    ax.set_ylim(-2, 2) # tan 그래프가 무한대로 가지 않게 y축 제한
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()


# --- Streamlit 앱 메인 부분 ---

st.title("✨ 삼각함수 시각화 애플리케이션")
st.write("학생들이 각도(θ)에 따라 사인, 코사인, 탄젠트 값이 어떻게 변하는지 직관적으로 이해할 수 있도록 돕는 도구입니다.")

# 사이드바에 슬라이더 추가
st.sidebar.header("각도(θ)를 조절하세요")
angle_deg1 = st.sidebar.slider("각도 (Degrees)", 0, 360, 45, 1, key="angle_slider1")

# 각도 변환 (Degree -> Radian)
angle_rad = np.radians(angle_deg1)

# 삼각함수 값 계산
sin_val = np.sin(angle_rad)
cos_val = np.cos(angle_rad)

# 탄젠트 값 계산 (90도, 270도 예외 처리)
if np.isclose(cos_val, 0):
    tan_val = None
    tan_str = "정의되지 않음 (무한대)"
else:
    tan_val = np.tan(angle_rad)
    tan_str = f"{tan_val:.4f}"

# 계산된 값 표시
st.header(f"선택된 각도: {angle_deg1}°")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Radian", value=f"{angle_rad:.4f}")
with col2:
    st.metric(label="Sine(θ)", value=f"{sin_val:.4f}")
with col3:
    st.metric(label="Cosine(θ)", value=f"{cos_val:.4f}")

st.metric(label="Tangent(θ)", value=tan_str)


st.markdown("---")


# 시각화 영역
st.header("시각화 자료")

# 2개의 그래프를 나란히 표시
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 왼쪽: 단위원
draw_unit_circle(ax1, angle_rad, sin_val, cos_val)

# 오른쪽: 삼각함수 그래프
draw_trig_functions(ax2, angle_rad, sin_val, cos_val, tan_val)

# Streamlit에 그래프 표시
st.pyplot(fig)

# 추가 설명
with st.expander("📝 학습 가이드 보기"):
    st.markdown("""
    #### 단위원 (왼쪽 그래프)
    - 반지름이 1인 원을 **단위원**이라고 합니다.
    - 원 위의 한 점의 **x좌표가 `cos(θ)` 값**이고, **y좌표가 `sin(θ)` 값**입니다.
    - 슬라이더를 움직이며 각도(θ)가 변할 때, 파란색 선(`cos`)과 초록색 선(`sin`)의 길이가 어떻게 변하는지 관찰해보세요.
    - 0도, 90도, 180도, 270도에서 `sin`과 `cos` 값이 어떻게 1, 0, -1이 되는지 확인해보세요.

    #### 삼각함수 그래프 (오른쪽 그래프)
    - 이 그래프는 각도(x축)에 따른 `sin`, `cos`, `tan`의 변화를 전체적으로 보여줍니다.
    - 슬라이더를 움직이면 현재 각도에 해당하는 위치에 **큰 점**이 표시됩니다.
    - 단위원에서 `sin` 값이 최대가 되는 90도에서, `sin` 그래프가 가장 높은 지점(1)에 도달하는 것을 볼 수 있습니다.
    - `tan` 함수는 `cos(θ)`가 0이 되는 90도(π/2)와 270도(3π/2)에서 값이 무한대로 가기 때문에 **점근선**을 가집니다.
    """)
    import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Matplotlib에서 한글 폰트가 깨지지 않도록 설정
# (실행 환경에 따라 폰트 경로를 확인해야 할 수 있습니다.)
# Windows: 'Malgun Gothic', macOS: 'AppleGothic', Linux: 'NanumGothic' 등
try:
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
except:
    # 대체 폰트 설정 (없을 경우 기본 폰트로 표시됨)
    pass


def draw_unit_circle(ax, angle_rad, sin_val, cos_val):
    """단위원과 각도에 따른 삼각형을 그리는 함수"""
    
    # 1. 단위원 그리기
    circle = patches.Circle((0, 0), radius=1, fill=False, color='black', linewidth=1.5)
    ax.add_patch(circle)

    # 2. x, y축 그리기
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.6)

    # 3. 각도에 해당하는 반지름(빗변) 그리기
    ax.plot([0, cos_val], [0, sin_val], 'r-', linewidth=2, label='반지름 (r=1)')

    # 4. cos(θ)와 sin(θ) 선분 그리기
    # cos(θ) - x축 성분 (밑변)
    ax.plot([0, cos_val], [0, 0], 'b-', linewidth=2, label=f'cos(θ) = {cos_val:.2f}')
    # sin(θ) - y축 성분 (높이)
    ax.plot([cos_val, cos_val], [0, sin_val], 'g-', linewidth=2, label=f'sin(θ) = {sin_val:.2f}')
    
    # 5. 각도 표시
    angle_deg = np.degrees(angle_rad)
    arc = patches.Arc((0, 0), 0.4, 0.4, angle=0, theta1=0, theta2=angle_deg, color='purple', linewidth=1.5)
    ax.add_patch(arc)
    ax.text(0.25 * np.cos(angle_rad / 2), 0.25 * np.sin(angle_rad / 2), f'θ', fontsize=12, color='purple')

    # 점 표시
    ax.plot(cos_val, sin_val, 'ro') # 반지름 끝점

    ax.set_title("단위원 시각화", fontsize=15)
    ax.legend(loc='upper right')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("cos(θ)")
    ax.set_ylabel("sin(θ)")


def draw_trig_functions(ax, angle_rad, sin_val, cos_val, tan_val):
    """삼각함수 그래프와 현재 각도 위치를 그리는 함수"""
    x = np.linspace(0, 2 * np.pi, 400)
    
    # 그래프 그리기
    ax.plot(x, np.sin(x), label='sin(x)', color='g')
    ax.plot(x, np.cos(x), label='cos(x)', color='b')
    ax.plot(x, np.tan(x), label='tan(x)', color='orange', linestyle='--')

    # 현재 각도 위치에 점 찍기
    ax.plot(angle_rad, sin_val, 'go', markersize=8)
    ax.plot(angle_rad, cos_val, 'bo', markersize=8)
    if tan_val is not None:
        ax.plot(angle_rad, tan_val, 'o', color='orange', markersize=8)

    ax.set_title("삼각함수 그래프", fontsize=15)
    ax.set_xlabel("각도 (Radian)")
    ax.set_ylabel("값")
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    ax.set_ylim(-2, 2) # tan 그래프가 무한대로 가지 않게 y축 제한
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()


# --- Streamlit 앱 메인 부분 ---

st.title("✨ 삼각함수 시각화 애플리케이션")
st.write("학생들이 각도(θ)에 따라 사인, 코사인, 탄젠트 값이 어떻게 변하는지 직관적으로 이해할 수 있도록 돕는 도구입니다.")

# 사이드바에 슬라이더 추가
st.sidebar.header("각도(θ)를 조절하세요")
angle_deg2 = st.sidebar.slider("각도 (Degrees)", 0, 360, 45, 1, key="angle_slider2")

# 각도 변환 (Degree -> Radian)
angle_rad = np.radians(angle_deg2)

# 삼각함수 값 계산
sin_val = np.sin(angle_rad)
cos_val = np.cos(angle_rad)

# 탄젠트 값 계산 (90도, 270도 예외 처리)
if np.isclose(cos_val, 0):
    tan_val = None
    tan_str = "정의되지 않음 (무한대)"
else:
    tan_val = np.tan(angle_rad)
    tan_str = f"{tan_val:.4f}"

# 계산된 값 표시
st.header(f"선택된 각도: {angle_deg2}°")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Radian", value=f"{angle_rad:.4f}")
with col2:
    st.metric(label="Sine(θ)", value=f"{sin_val:.4f}")
with col3:
    st.metric(label="Cosine(θ)", value=f"{cos_val:.4f}")

st.metric(label="Tangent(θ)", value=tan_str)


st.markdown("---")


# 시각화 영역
st.header("시각화 자료")

# 2개의 그래프를 나란히 표시
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 왼쪽: 단위원
draw_unit_circle(ax1, angle_rad, sin_val, cos_val)

# 오른쪽: 삼각함수 그래프
draw_trig_functions(ax2, angle_rad, sin_val, cos_val, tan_val)

# Streamlit에 그래프 표시
st.pyplot(fig)

# 추가 설명
with st.expander("📝 학습 가이드 보기"):
    st.markdown("""
    #### 단위원 (왼쪽 그래프)
    - 반지름이 1인 원을 **단위원**이라고 합니다.
    - 원 위의 한 점의 **x좌표가 `cos(θ)` 값**이고, **y좌표가 `sin(θ)` 값**입니다.
    - 슬라이더를 움직이며 각도(θ)가 변할 때, 파란색 선(`cos`)과 초록색 선(`sin`)의 길이가 어떻게 변하는지 관찰해보세요.
    - 0도, 90도, 180도, 270도에서 `sin`과 `cos` 값이 어떻게 1, 0, -1이 되는지 확인해보세요.

    #### 삼각함수 그래프 (오른쪽 그래프)
    - 이 그래프는 각도(x축)에 따른 `sin`, `cos`, `tan`의 변화를 전체적으로 보여줍니다.
    - 슬라이더를 움직이면 현재 각도에 해당하는 위치에 **큰 점**이 표시됩니다.
    - 단위원에서 `sin` 값이 최대가 되는 90도에서, `sin` 그래프가 가장 높은 지점(1)에 도달하는 것을 볼 수 있습니다.
    - `tan` 함수는 `cos(θ)`가 0이 되는 90도(π/2)와 270도(3π/2)에서 값이 무한대로 가기 때문에 **점근선**을 가집니다.
    """)