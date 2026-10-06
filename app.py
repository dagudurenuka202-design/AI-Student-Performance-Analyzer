import streamlit as st
from analyzer import analyze_student
from chatbot import get_chatbot_response
from rag import process_pdf, search_knowledge

st.set_page_config(
    page_title="AI Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Student Performance Analyzer")
st.write("Analyze your academic performance and get personalized AI study guidance.")

# ---------------- SIDEBAR ----------------

st.sidebar.header("📚 Student Information")

name = st.sidebar.text_input("Student Name", "Student")

subjects = st.sidebar.text_area(
    "Subjects and Marks",
    "Mathematics: 75\nPhysics: 68\nComputer Science: 85\nEnglish: 80"
)

attendance = st.sidebar.number_input(
    "Attendance (%)",
    min_value=0.0,
    max_value=100.0,
    value=80.0
)

study_hours = st.sidebar.number_input(
    "Average Study Hours/Day",
    min_value=0.0,
    max_value=24.0,
    value=3.0
)

strengths = st.text_area(
    "Your Strengths",
    "Programming, English"
)

weaknesses = st.text_area(
    "Your Weaknesses",
    "Mathematics, concentration"
)

# ---------------- ANALYSIS ----------------

st.header("📊 Performance Analysis")

if st.button("🔍 Analyze My Performance"):

    student_data = {
        "name": name,
        "subjects": subjects,
        "attendance": attendance,
        "study_hours": study_hours,
        "strengths": strengths,
        "weaknesses": weaknesses
    }

    with st.spinner("AI is analyzing your performance..."):

        result = analyze_student(student_data)

    st.subheader("🤖 AI Analysis")

    st.markdown(result)


# ---------------- PDF UPLOAD ----------------

st.header("📄 Upload Study Material")

uploaded_file = st.file_uploader(
    "Upload a PDF such as syllabus, notes or study material",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Processing PDF..."):

        chunks = process_pdf(uploaded_file)

    st.success(f"PDF processed successfully! {len(chunks)} sections found.")


# ---------------- CHATBOT ----------------

st.header("💬 AI Student Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_question = st.chat_input(
    "Ask something about your performance or studies..."
)

if user_question:

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # Search uploaded knowledge
    context = search_knowledge(user_question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = get_chatbot_response(
                user_question,
                context
            )

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })