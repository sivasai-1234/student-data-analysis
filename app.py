import streamlit as st
import pandas as pd
import plotly.express as px
import io
from reportlab.pdfgen import canvas

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)

# =========================
# UI STYLE
# =========================

st.markdown("""
<style>

body {
background-color:#f5f7fb;
}

.big-title{
font-size:42px;
font-weight:700;
color:#1f4e79;
text-align:center;
margin-bottom:20px;
}

.metric-card{
background-color:white;
padding:20px;
border-radius:12px;
box-shadow:0px 4px 12px rgba(0,0,0,0.1);
text-align:center;
}

.metric-number{
font-size:28px;
font-weight:bold;
color:#1f4e79;
}

.metric-label{
font-size:14px;
color:#555;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN SESSION
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN FUNCTION
# =========================

def login():

    st.markdown('<div class="big-title">🎓 Student Performance Analyzer</div>', unsafe_allow_html=True)

    st.subheader("Teacher Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "teacher" and password == "1234":

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("Invalid login credentials")

# =========================
# AI COMMENT FUNCTION
# =========================

def student_comment(score):

    if score >= 90:
        return "Excellent performance"
    elif score >= 75:
        return "Very good understanding"
    elif score >= 60:
        return "Good but needs improvement"
    elif score >= 50:
        return "Needs serious improvement"
    else:
        return "At risk of failing"

# =========================
# DASHBOARD
# =========================

def dashboard():

    st.markdown('<div class="big-title">📊 Teacher Analytics Dashboard</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # FILE UPLOAD

    st.sidebar.header("Upload Student File")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel or CSV",
        type=["xlsx","csv"]
    )

    # MULTI CLASS

    st.sidebar.header("Multi-Class Comparison")

    multi_files = st.sidebar.file_uploader(
        "Upload Multiple Class Files",
        type=["xlsx","csv"],
        accept_multiple_files=True
    )

    if uploaded_file:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # MID MARKS

        df["Mid_Final"] = df.apply(
            lambda row: 0.8 * max(row["Mid1"],row["Mid2"]) + 0.2 * min(row["Mid1"],row["Mid2"]),
            axis=1
        )

        # TOTAL

        df["Total"] = df["Assignment"] + df["Mid_Final"] + df["Semester"]

        # GRADES

        def grade(total):

            if total >= 90:
                return "A"
            elif total >= 75:
                return "B"
            elif total >= 60:
                return "C"
            elif total >= 50:
                return "D"
            else:
                return "F"

        df["Grade"] = df["Total"].apply(grade)

        # RANKING

        df["Rank"] = df["Total"].rank(method="min", ascending=False).astype(int)

        df = df.sort_values("Rank")

        # AI COMMENTS

        df["Feedback"] = df["Total"].apply(student_comment)

        # METRICS

        students = len(df)
        avg = round(df["Total"].mean(),2)
        highest = round(df["Total"].max(),2)
        lowest = round(df["Total"].min(),2)

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-number">{students}</div>
            <div class="metric-label">Students</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-number">{avg}</div>
            <div class="metric-label">Average</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-number">{highest}</div>
            <div class="metric-label">Highest</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-number">{lowest}</div>
            <div class="metric-label">Lowest</div>
            </div>
            """, unsafe_allow_html=True)

        # PASS FAIL

        pass_percent = round(len(df[df["Grade"]!="F"])/students*100,2)
        fail_percent = round(len(df[df["Grade"]=="F"])/students*100,2)

        st.subheader("📊 Class Result Summary")

        c1,c2 = st.columns(2)

        c1.metric("Pass %",f"{pass_percent}%")
        c2.metric("Fail %",f"{fail_percent}%")

        # SUBJECT PERFORMANCE

        st.subheader("📚 Subject Performance")

        subject_avg = pd.DataFrame({
            "Category":["Assignment","Mid Exams","Semester"],
            "Average":[
                df["Assignment"].mean(),
                df["Mid_Final"].mean(),
                df["Semester"].mean()
            ]
        })

        fig = px.bar(subject_avg,x="Category",y="Average",text_auto=True)

        st.plotly_chart(fig)

        # FAILING STUDENTS

        st.subheader("⚠ Failing Students")

        fail_df = df[df["Grade"]=="F"]

        if len(fail_df)>0:

            st.error(f"{len(fail_df)} students failing")

            st.table(fail_df[["Name","Total","Grade"]])

        else:

            st.success("No failing students")

        # SEARCH

        st.subheader("🔍 Search Student")

        search = st.text_input("Enter name")

        filtered = df

        if search:

            filtered = df[df["Name"].str.contains(search,case=False)]

        st.dataframe(filtered)

        # TOP STUDENTS

        st.subheader("🏆 Top 5 Students")

        st.table(df.head(5)[["Rank","Name","Total","Grade"]])

        # GRADE PIE

        st.subheader("📈 Grade Distribution")

        pie = px.pie(df,names="Grade")

        st.plotly_chart(pie)

        # STUDENT FEEDBACK

        st.subheader("🧠 AI Student Feedback")

        st.table(df[["Name","Total","Grade","Feedback"]])

        # DOWNLOAD EXCEL

        st.subheader("📥 Download Excel Report")

        buffer = io.BytesIO()

        df.to_excel(buffer,index=False,engine="openpyxl")

        buffer.seek(0)

        st.download_button(
            "Download Excel",
            buffer,
            file_name="student_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # PDF REPORT

        st.subheader("📄 Download PDF Report")

        def create_pdf():

            buffer = io.BytesIO()

            c = canvas.Canvas(buffer)

            c.drawString(200,800,"Student Performance Report")

            c.drawString(100,760,f"Students: {students}")
            c.drawString(100,740,f"Average: {avg}")
            c.drawString(100,720,f"Highest: {highest}")
            c.drawString(100,700,f"Lowest: {lowest}")

            c.save()

            buffer.seek(0)

            return buffer

        pdf = create_pdf()

        st.download_button(
            "Download PDF",
            pdf,
            file_name="class_report.pdf",
            mime="application/pdf"
        )

    # MULTI CLASS

    if multi_files:

        st.header("🏫 Multi-Class Comparison")

        class_data = []

        for file in multi_files:

            if file.name.endswith(".csv"):
                temp = pd.read_csv(file)
            else:
                temp = pd.read_excel(file)

            temp["Mid_Final"] = temp.apply(
                lambda row: 0.8 * max(row["Mid1"],row["Mid2"]) + 0.2 * min(row["Mid1"],row["Mid2"]),
                axis=1
            )

            temp["Total"] = temp["Assignment"] + temp["Mid_Final"] + temp["Semester"]

            avg = temp["Total"].mean()

            class_data.append({
                "Class":file.name,
                "Average":avg
            })

        class_df = pd.DataFrame(class_data)

        fig = px.bar(class_df,x="Class",y="Average",text_auto=True)

        st.plotly_chart(fig)

        best = class_df.loc[class_df["Average"].idxmax()]

        st.success(f"Best Performing Class: {best['Class']}")

# =========================
# APP CONTROL
# =========================

if st.session_state.logged_in:
    dashboard()
else:
    login()