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

if "saved_pace" not in st.session_state:
    st.session_state.saved_pace = 0


# ---------------- STYLING ----------------
st.markdown("""
<style>

.stApp{
    background-color:#626BC5;
}

html, body, [class*="css"]{
    font-family: 'Arial';
    color:#F7EEDF;
}

.block-container{
    padding-top:2rem;
}

.title{
    text-align:center;
    font-size:58px;
    font-weight:700;
    color:#F7EEDF;
    margin-bottom:40px;
}

.timer-circle{
    width:320px;
    height:320px;
    border:5px solid #F7EEDF;
    border-radius:50%;
    margin:auto;

    display:flex;
    justify-content:center;
    align-items:center;

    font-size:72px;
    font-weight:700;
    color:#F7EEDF;
}

.summary-title{
    text-align:center;
    font-size:32px;
    margin-top:30px;
    color:#F7EEDF;
}

.summary-value{
    text-align:center;
    font-size:72px;
    font-weight:700;
    margin-bottom:30px;
    color:#F7EEDF;
}

.book{
    text-align:center;
    font-size:180px;
}

div.stButton > button{
    border-radius:999px;
    height:55px;
    font-size:22px;
    font-weight:700;
    border:none;
    background:linear-gradient(90deg,#B9BCE8,#F1F1F1);
    color:#27348B;
}

div.stButton > button:hover{
    background:linear-gradient(90deg,#D7D9F6,#FFFFFF);
    color:#27348B;
}

.stNumberInput label{
    color:#F7EEDF !important;
    font-size:20px !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TIMER PAGE ----------------
if not st.session_state.show_summary:

    st.markdown(
        "<div class='title'>Let's read</div>",
        unsafe_allow_html=True
    )

    elapsed = st.session_state.elapsed

    if st.session_state.running:
        elapsed = int(time.time() - st.session_state.start_time)
        st.session_state.elapsed = elapsed
        st.rerun()

    minutes = elapsed // 60
    seconds = elapsed % 60

    st.markdown(
        f"""
        <div class="timer-circle">
            {minutes:02}:{seconds:02}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start", use_container_width=True):

            st.session_state.running = True
            st.session_state.start_time = (
                time.time() - st.session_state.elapsed
            )

            st.rerun()

    with col2:
        if st.button("Stop", use_container_width=True):

            st.session_state.running = False
            st.rerun()

    st.write("")
    st.write("")

    pages = st.number_input(
        "Pages Read",
        min_value=1,
        step=1
    )

    # muncul setelah stop
    if not st.session_state.running and st.session_state.elapsed > 0:

        st.write("")

        if st.button("Save Reading", use_container_width=True):

            total_minutes = st.session_state.elapsed / 60

            if total_minutes > 0:
                pace = pages / total_minutes
            else:
                pace = 0

            st.session_state.saved_pages = pages
            st.session_state.saved_pace = pace
            st.session_state.show_summary = True

            st.rerun()


# ---------------- SUMMARY PAGE ----------------
else:

    elapsed = st.session_state.elapsed

    minutes = elapsed // 60
    seconds = elapsed % 60

    st.markdown(
        "<div class='summary-title'>Distance</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='summary-value'>{st.session_state.saved_pages} pages</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='summary-title'>Pace</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='summary-value'>{st.session_state.saved_pace:.1f} / pages</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='summary-title'>Time</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='summary-value'>{minutes} s</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='book'>📖</div>",
        unsafe_allow_html=True
    )

    if st.button("Start New Reading", use_container_width=True):

        st.session_state.running = False
        st.session_state.start_time = None
        st.session_state.elapsed = 0
        st.session_state.show_summary = False

        st.rerun()
