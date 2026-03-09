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
# STYLE (Animated Landing + Button + Cards)
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
    background: linear-gradient(-45deg,#1f4e79,#4f8cc9,#2c6fb3,#1f4e79);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}
@keyframes gradientMove { 0% {background-position:0% 50%;} 50% {background-position:100% 50%;} 100% {background-position:0% 50%;}}
.big-title{ font-size:44px; font-weight:800; color:white; text-align:center; margin-bottom:30px;}
.feature-card{ background: rgba(255,255,255,0.9); padding:25px; border-radius:14px; text-align:center; box-shadow:0px 8px 20px rgba(0,0,0,0.25); color:#222; transition: transform 0.3s;}
.feature-card:hover{ transform: translateY(-6px);}
.login-card{ background:white; padding:40px; border-radius:15px; box-shadow:0px 10px 25px rgba(0,0,0,0.2); text-align:center;}
div.stButton > button{ display:block; margin-left:auto; margin-right:auto; font-size:22px; padding:14px 35px; border-radius:12px; background: linear-gradient(45deg,#ffcc00,#ff9900); color:black; border:none; font-weight:bold; transition: all 0.3s ease; box-shadow:0px 6px 18px rgba(0,0,0,0.3);}
div.stButton > button:hover{ transform: scale(1.08); box-shadow:0px 10px 25px rgba(0,0,0,0.4); background: linear-gradient(45deg,#ffd633,#ff9900);}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "start_app_clicked" not in st.session_state:
    st.session_state.start_app_clicked = False

# =========================
# LANDING PAGE
# =========================
def landing_page():
    st.markdown('<div class="big-title">🎓 Student Performance Analyzer</div>', unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card"><h3>📊 Analytics</h3>Visualize student performance instantly</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><h3>🤖 AI Feedback</h3>Automatic teacher comments</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card"><h3>📄 Reports</h3>Export Excel and PDF reports</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Start Application", key="start_app"):
        st.session_state.show_login = True
        st.session_state.start_app_clicked = True

# =========================
# LOGIN
# =========================
def login():
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="big-title">Teacher Login</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        users = {"teacher":"1234","admin":"admin123"}
        if st.button("Login", key="login_btn"):
            if username in users and password==users[username]:
                st.session_state.logged_in = True
                st.session_state.show_login = False
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# STUDENT COMMENT
# =========================
def student_comment(score):
    if score>=90: return "Excellent performance"
    elif score>=75: return "Very good understanding"
    elif score>=60: return "Good but needs improvement"
    elif score>=50: return "Needs improvement"
    else: return "At risk of failing"

# =========================
# DASHBOARD AND OTHER PAGES
# =========================
def dashboard():
    with st.sidebar:
        st.title("🎓 Teacher Panel")
        menu = st.radio("Navigation", ["Dashboard","Student Analytics","Student Profile","Reports","Class Comparison","Settings"])
        uploaded_file = st.file_uploader("Upload Student File", type=["xlsx","csv"])
        multi_files = st.file_uploader("Upload Multiple Classes", type=["xlsx","csv"], accept_multiple_files=True)
    
    if uploaded_file:
        # Load file
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        df.columns = df.columns.str.replace("_","").str.strip()
        df["Mid_Final"] = df.apply(lambda r: 0.8*max(r["Mid1"],r["Mid2"])+0.2*min(r["Mid1"],r["Mid2"]), axis=1)
        df["Total"] = df["Assignment"]+df["Mid_Final"]+df["Semester"]
        df["Grade"] = df["Total"].apply(lambda t:"A" if t>=90 else "B" if t>=75 else "C" if t>=60 else "D" if t>=50 else "F")
        df["Rank"] = df["Total"].rank(method="min", ascending=False).astype(int)
        df["Feedback"] = df["Total"].apply(student_comment)
        if "RollNo" in df.columns: df = df.sort_values("RollNo")
        students=len(df); avg=round(df["Total"].mean(),2); highest=round(df["Total"].max(),2); lowest=round(df["Total"].min(),2)
    
        # ========== Dashboard ==========
        if menu=="Dashboard":
            st.title("📊 Dashboard")
            col1,col2,col3,col4 = st.columns(4)
            col1.metric("Students",students)
            col2.metric("Average",avg)
            col3.metric("Highest",highest)
            col4.metric("Lowest",lowest)
            topper = df.loc[df["Total"].idxmax()]["Name"]
            weakest = df.loc[df["Total"].idxmin()]["Name"]
            performance = "Strong" if avg>70 else "Moderate" if avg>55 else "Needs Improvement"
            st.markdown(f"<div style='background:white;padding:25px;border-radius:12px;color:black;box-shadow:0px 5px 15px rgba(0,0,0,0.2);margin-top:20px;'><h4>📊 Class Insight</h4><p><b>Top performer:</b> {topper}</p><p><b>Average class score:</b> {avg}</p><p><b>Student needing most support:</b> {weakest}</p><p><b>Overall class performance:</b> {performance}</p></div>", unsafe_allow_html=True)

        # ========== Student Analytics ==========
        if menu=="Student Analytics":
            st.title("👨‍🎓 Student Analytics")
            st.subheader("Leaderboard")
            st.dataframe(df[["RollNo","Rank","Name","Total","Grade"]].style.set_properties(**{'text-align': 'center'}), hide_index=True)
            st.subheader("🏆 Top Performers")
            top_students = df.sort_values("Total", ascending=False).head(3)
            medals = ["🥇","🥈","🥉"]
            for i,row in top_students.reset_index().iterrows():
                st.write(f"{medals[i]} {row['Name']} | Score: {round(row['Total'],2)}")
            st.subheader("Grade Distribution")
            st.plotly_chart(px.pie(df,names="Grade",hole=0.4))
            st.subheader("Performance Trend")
            st.plotly_chart(px.line(df,x="RollNo",y="Total",markers=True))
            st.subheader("AI Feedback")
            st.table(df[["RollNo","Name","Total","Grade","Feedback"]].style.set_properties(**{'text-align': 'center'}))
            st.subheader("⚠ At-Risk Students")
            risk_students = df[df["Total"]<50]
            if len(risk_students)>0:
                st.dataframe(risk_students[["RollNo","Name","Total","Grade"]].style.set_properties(**{'text-align': 'center'}), hide_index=True)
            else:
                st.success("No at-risk students 🎉")

        # ========== Student Profile ==========
        if menu=="Student Profile":
            st.title("👤 Student Profile")
            search_choice = st.radio("Search By", ["Name","Roll Number"])
            if search_choice=="Name":
                student = st.selectbox("Select Student", df["Name"])
                student_data = df[df["Name"]==student].iloc[0]
            else:
                roll = st.selectbox("Select Roll Number", df["RollNo"])
                student_data = df[df["RollNo"]==roll].iloc[0]
            col1,col2,col3 = st.columns(3)
            col1.metric("Total Marks", round(student_data["Total"],2))
            col2.metric("Grade", student_data["Grade"])
            col3.metric("Rank", student_data["Rank"])
            marks_df = pd.DataFrame({"Category":["Assignment","Mid","Semester"],"Marks":[student_data["Assignment"],student_data["Mid_Final"],student_data["Semester"]]})
            st.plotly_chart(px.bar(marks_df,x="Category",y="Marks",text_auto=True))
            st.success(student_data["Feedback"])

        # ========== Reports ==========
        if menu=="Reports":
            st.title("📄 Reports")
            st.dataframe(df.style.set_properties(**{'text-align': 'center'}), hide_index=True)
            buffer = io.BytesIO()
            df.to_excel(buffer,index=False)
            buffer.seek(0)
            st.download_button("Download Excel", buffer, file_name="report.xlsx")
            def create_pdf():
                buffer = io.BytesIO()
                c = canvas.Canvas(buffer)
                c.drawString(200,800,"Student Report")
                c.drawString(100,760,f"Students: {students}")
                c.drawString(100,740,f"Average: {avg}")
                c.drawString(100,720,f"Highest: {highest}")
                c.drawString(100,700,f"Lowest: {lowest}")
                c.save()
                buffer.seek(0)
                return buffer
            st.download_button("Download PDF", create_pdf(), file_name="report.pdf")

        # ========== Class Comparison ==========
        if menu=="Class Comparison" and multi_files:
            st.title("🏫 Class Comparison")
            class_data=[]
            for file in multi_files:
                temp = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
                temp["Mid_Final"] = temp.apply(lambda r: 0.8*max(r["Mid1"],r["Mid2"])+0.2*min(r["Mid1"],r["Mid2"]), axis=1)
                temp["Total"] = temp["Assignment"]+temp["Mid_Final"]+temp["Semester"]
                class_data.append({"Class":file.name,"Average":temp["Total"].mean()})
            st.plotly_chart(px.bar(pd.DataFrame(class_data),x="Class",y="Average",text_auto=True))

        # ========== Settings ==========
        if menu=="Settings":
            st.title("⚙ Settings")
            if st.button("Logout"):
                st.session_state.logged_in=False
                st.session_state.show_login=False
                st.session_state.start_app_clicked=False

# =========================
# APP CONTROL
# =========================
if st.session_state.logged_in:
    dashboard()
elif st.session_state.show_login or st.session_state.start_app_clicked:
    login()
else:
    landing_page()