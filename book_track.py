
import streamlit as st
import time

st.set_page_config(
    page_title="Reading Tracker",
    page_icon="📚",
    layout="centered"
)

if "running" not in st.session_state:
    st.session_state.running = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0


st.markdown("""
<style>
.main {
    background-color: #0f1117;
}

.block-container {
    padding-top: 2rem;
}

.timer-card {
    background: #1b1f2a;
    padding: 30px;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 20px;
    border: 1px solid #2d3345;
}

.result-card {
    background: #1b1f2a;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #2d3345;
}

.big-timer {
    font-size: 52px;
    font-weight: bold;
    color: white;
}

.subtitle {
    color: #9ca3af;
    text-align: center;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;'>📚 Reading Tracker</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Track your reading session beautifully ✨</p>",
    unsafe_allow_html=True
)

with st.container():
    st.markdown("<div class='timer-card'>", unsafe_allow_html=True)

    elapsed = st.session_state.elapsed

    if st.session_state.running:
        elapsed = int(time.time() - st.session_state.start_time)
        st.session_state.elapsed = elapsed

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    st.markdown(
        f"<div class='big-timer'>{hours:02}:{minutes:02}:{seconds:02}</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Start", use_container_width=True):
            st.session_state.running = True
            st.session_state.start_time = time.time() - st.session_state.elapsed

    with col2:
        if st.button("⏹ Stop", use_container_width=True):
            st.session_state.running = False

    st.markdown("</div>", unsafe_allow_html=True)

pages = st.number_input(
    "📖 Total Pages Read",
    min_value=1,
    step=1
)

if st.button("Calculate Reading Stats", use_container_width=True):

    total_minutes = st.session_state.elapsed / 60

    if total_minutes > 0:
        avg_speed = pages / total_minutes
    else:
        avg_speed = 0

    st.markdown("<div class='result-card'>", unsafe_allow_html=True)

    st.markdown("## ✨ Reading Summary")

    st.write(f"⏱ **Reading Time:** {hours:02}:{minutes:02}:{seconds:02}")
    st.write(f"📚 **Pages Read:** {pages} pages")
    st.write(f"⚡ **Average Speed:** {avg_speed:.2f} pages/minute")

    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Made with Streamlit 💖")
