import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(
    page_title="🎮 Android 게임 데이터 대시보드 - Cyberpunk",
    layout="wide",
    page_icon="🎮",
)

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

/* 전체 배경 */
body {
    background: linear-gradient(135deg, #0a0a0a, #1b1b40, #2a0a5e);
    color: #00ffff;
    font-family: 'Orbitron', sans-serif;
}

/* 제목 h1, h2, h3 */
h1, h2, h3 {
    color: #00ffff !important;
    text-shadow: 0 0 5px #00ffff, 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 30px #00ffff;
    font-family: 'Orbitron', sans-serif !important;
}

/* 일반 텍스트 */
.stMarkdown, .stText, .stDataFrame, div, p, label, span {
    color: #ffffff !important;
    font-family: 'Orbitron', sans-serif;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #1b1b40;
    border-right: 2px solid #00ffff;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* 버튼 네온 스타일 */
.stButton>button {
    background: linear-gradient(45deg, #00ffff, #ff00ff);
    color: white;
    font-weight: bold;
    border: 2px solid #ff00ff;
    box-shadow: 0 0 10px #00ffff, 0 0 20px #ff00ff;
    transition: 0.3s;
}
.stButton>button:hover {
    box-shadow: 0 0 20px #00ffff, 0 0 40px #ff00ff, 0 0 60px #00ffff;
}
</style>
""", unsafe_allow_html=True)

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("android-games.csv")
    if 'Installs' in df.columns:
        df['Installs'] = df['Installs'].astype(str).str.replace(',','').str.replace('+','').astype(int)
    return df

df = load_data()

# --- 제목 ---
st.title("🎮 Android 게임 데이터 대시보드 - Cyberpunk")
st.markdown("##### 파란/보라/검정 사이버펑크 네온 스타일로 Android 게임 데이터를 분석")

# --- 탭 ---
tab1, tab2, tab3 = st.tabs(["📄 데이터 요약", "📊 시각화", "💡 인사이트"])

# ==============================
# 📄 데이터 요약
# ==============================
with tab1:
    st.subheader("📋 데이터 개요")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 데이터 수", len(df))
    col2.metric("컬럼 개수", len(df.columns))
    col3.metric("결측치 포함 여부", "✅ 없음" if df.isna().sum().sum()==0 else "⚠️ 있음")

    with st.expander("🔍 데이터 미리보기"):
        st.dataframe(df.head(), use_container_width=True)

# ==============================
# 📊 시각화
# ==============================
with tab2:
    st.sidebar.header("⚙️ 시각화 설정")
    numeric_columns = df.select_dtypes(include=['int64','float64']).columns.tolist()
    y_axis = st.sidebar.selectbox("Y축 (숫자형)", numeric_columns, index=numeric_columns.index('Rating') if 'Rating' in numeric_columns else 0)

    st.subheader(f"📊 막대 그래프: Installs vs {y_axis}")

    # 상위 50개 앱 데이터
    df_sorted = df.sort_values(by=y_axis, ascending=False).head(50)

    # 기본 막대
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_sorted['Installs'],
        y=df_sorted[y_axis],
        marker=dict(
            color=df_sorted[y_axis],
            colorscale='Plasma',
            line=dict(color='#ff00ff', width=1.5)  # 기본 막대 테두리 네온
        ),
        text=df_sorted[y_axis],
        textposition='outside'
    ))

    # 상위 10개 앱 강조
    top10 = df_sorted.head(10)
    fig.add_trace(go.Bar(
        x=top10['Installs'],
        y=top10[y_axis],
        marker=dict(
            color='rgba(0,255,255,0.8)',
            line=dict(color='#ff00ff', width=4)
        ),
        text=top10[y_axis],
        textposition='outside',
        name='Top 10 네온 강조'
    ))

    fig.update_layout(
        yaxis_title=y_axis,
        font=dict(color="#00ffff", family="Orbitron"),
        title_font=dict(color="#ff00ff", family="Orbitron"),
        legend_title_font=dict(color="#ff00ff"),
        legend_font=dict(color="#00ffff"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"🏆 {y_axis} 기준 상위 10개 앱")
    st.dataframe(top10[['Installs', y_axis]], use_container_width=True)

# ==============================
# 💡 인사이트
# ==============================
with tab3:
    st.subheader("💡 데이터 인사이트")
    if not df.empty:
        numeric_cols = df.select_dtypes(include=['int64','float64']).columns
        for col in numeric_cols:
            max_val, min_val, mean_val = df[col].max(), df[col].min(), df[col].mean()
            st.write(f"- **{col}** → 최고: {max_val:.2f}, 최저: {min_val:.2f}, 평균: {mean_val:.2f}")

        st.markdown("---")
        st.markdown("""
        📈 **요약:**  
        - 다운로드 수 상위 앱들은 평점과 리뷰 수에서도 높은 경향을 보임  
        - 상위 앱 데이터로 인기 게임 트렌드 확인 가능  
        - 막대그래프 + 네온 강조로 앱별 성능 비교 및 전략 활용  

        🎯 **활용 팁:**  
        - X축: 다운로드 수, Y축: 평점/리뷰 수로 인기 앱 분석 가능  
        - Top 10 앱 강조로 장르별 트렌드 분석 가능  
        - 앱 추천, 마케팅, 신규 게임 기획에 활용 가능
        """)
