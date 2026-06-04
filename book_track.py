import streamlit as st
import time

st.set_page_config(
    page_title="Let's Read",
    page_icon="📚",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "running" not in st.session_state:
    st.session_state.running = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0

if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

if "saved_pages" not in st.session_state:
    st.session_state.saved_pages = 0

if "saved_pace_seconds" not in st.session_state:
    st.session_state.saved_pace_seconds = 0


# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background-color: #626BC5;
}

.block-container {
    padding-top: 1rem;
    max-width: 900px;
}

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
    color: #F7EEDF;
}

.title {
    text-align: center;
    font-size: 64px;
    font-weight: 800;
    color: #F7EEDF;
    margin-bottom: 55px;
}

.timer-circle {
    width: 330px;
    height: 330px;
    border: 6px solid #F7EEDF;
    border-radius: 50%;
    margin: auto;

    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 74px;
    font-weight: 800;
    color: #F7EEDF;
}

.button-space {
    margin-top: 55px;
}

div.stButton > button {
    border-radius: 999px;
    height: 60px;
    font-size: 22px;
    font-weight: 700;
    border: none;
    background: linear-gradient(90deg, #D8DAF7, #FFFFFF);
    color: #1F2A8A;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #FFFFFF, #E8E9FF);
    color: #1F2A8A;
}

.stNumberInput label {
    color: #F7EEDF !important;
    font-size: 20px !important;
    font-weight: 700 !important;
}

.summary-label {
    text-align: center;
    font-size: 30px;
    color: #F7EEDF;
    font-weight: 500;
    margin-top: 20px;
}

.summary-value {
    text-align: center;
    font-size: 68px;
    color: #F7EEDF;
    font-weight: 800;
    margin-bottom: 25px;
}

.book {
    text-align: center;
    font-size: 160px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HELPER ----------------
def format_timer(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02}:{remaining_seconds:02}"


def format_time_summary(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    if minutes > 0:
        return f"{minutes} m {remaining_seconds} s"
    return f"{remaining_seconds} s"


def format_pace(seconds_per_page):
    seconds_per_page = int(round(seconds_per_page))
    minutes = seconds_per_page // 60
    seconds = seconds_per_page % 60

    if minutes > 0:
        return f"{minutes}'{seconds:02}'' / page"
    return f"{seconds}'' / page"


# ---------------- TIMER PAGE ----------------
if not st.session_state.show_summary:

    st.markdown("<div class='title'>Let's read</div>", unsafe_allow_html=True)

    if st.session_state.running:
        st.session_state.elapsed = int(time.time() - st.session_state.start_time)

    elapsed = st.session_state.elapsed

    st.markdown(
        f"""
        <div class="timer-circle">
            {format_timer(elapsed)}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='button-space'></div>", unsafe_allow_html=True)

    # SATU TOMBOL: START / STOP
    if st.session_state.running:
        button_text = "Stop"
    else:
        button_text = "Start"

    if st.button(button_text, use_container_width=True):
        if st.session_state.running:
            # STOP
            st.session_state.elapsed = int(time.time() - st.session_state.start_time)
            st.session_state.running = False
        else:
            # START / RESUME
            st.session_state.running = True
            st.session_state.start_time = time.time() - st.session_state.elapsed

        st.rerun()

    # muncul setelah stop
    if not st.session_state.running and st.session_state.elapsed > 0:

        st.write("")
        st.write("")

        pages = st.number_input(
            "Pages Read",
            min_value=1,
            step=1
        )

        if st.button("Save Reading", use_container_width=True):
            pace_seconds = st.session_state.elapsed / pages

            st.session_state.saved_pages = pages
            st.session_state.saved_pace_seconds = pace_seconds
            st.session_state.show_summary = True

            st.rerun()

    # Auto-refresh sederhana tanpa package tambahan
    if st.session_state.running:
        time.sleep(1)
        st.rerun()


# ---------------- SUMMARY PAGE ----------------
else:

    elapsed = st.session_state.elapsed

    st.markdown(
        "<div class='summary-label'>Distance</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='summary-value'>{st.session_state.saved_pages} pages</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='summary-label'>Pace</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='summary-value'>{format_pace(st.session_state.saved_pace_seconds)}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='summary-label'>Time</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='summary-value'>{format_time_summary(elapsed)}</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='book'>📖</div>", unsafe_allow_html=True)

    if st.button("Start New Reading", use_container_width=True):
        st.session_state.running = False
        st.session_state.start_time = None
        st.session_state.elapsed = 0
        st.session_state.show_summary = False
        st.session_state.saved_pages = 0
        st.session_state.saved_pace_seconds = 0

        st.rerun()
