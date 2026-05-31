import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw
import io

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="EduVision Pro",
    layout="wide",
    page_icon="🎓"
)

# =========================
# DATA
# =========================
if "students" not in st.session_state:
    st.session_state.students = [
        {
            "id": 1,
            "name": "Rahul",
            "class": "10A",
            "attendance": 92,
            "blood_group": "O+",
            "phone": "9876543210",
            "parent_phone": "9123456780",
            "address": "Delhi",
            "avatar": "👨‍🎓",
            "subjects": {"Maths": 88, "Science": 82, "English": 79, "Social": 91, "Computer": 95}
        },
        {
            "id": 2,
            "name": "Sneha",
            "class": "10A",
            "attendance": 88,
            "blood_group": "A+",
            "phone": "9876543211",
            "parent_phone": "9123456781",
            "address": "Mumbai",
            "avatar": "👩‍🎓",
            "subjects": {"Maths": 75, "Science": 80, "English": 82, "Social": 70, "Computer": 88}
        },
        {
            "id": 3,
            "name": "Amit",
            "class": "10B",
            "attendance": 95,
            "blood_group": "B+",
            "phone": "9876543212",
            "parent_phone": "9123456782",
            "address": "Bangalore",
            "avatar": "🧑‍🎓",
            "subjects": {"Maths": 90, "Science": 93, "English": 85, "Social": 88, "Computer": 96}
        }
    ]

# =========================
# SAFE DATAFRAME
# =========================
def build_df():
    rows = []

    for s in st.session_state.students:
        sub = s["subjects"]

        rows.append({
            "name": s["name"],
            "class": s["class"],
            "attendance": s["attendance"],
            "blood_group": s["blood_group"],
            "phone": s["phone"],
            "parent_phone": s["parent_phone"],
            "address": s["address"],
            "avatar": s["avatar"],
            "Maths": sub["Maths"],
            "Science": sub["Science"],
            "English": sub["English"],
            "Social": sub["Social"],
            "Computer": sub["Computer"],
            "avg_marks": sum(sub.values()) / len(sub)
        })

    return pd.DataFrame(rows)

df = build_df()

# =========================
# UI STYLE
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #052e16, #064e3b, #022c22);
}

.title {
    font-size: 44px;
    font-weight: bold;
    text-align: center;
    color: #22c55e;
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 18px;
    margin: 12px 0;
    color: white;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎓 EduVision Pro Analytics System</div>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Students", "Add Student", "Analytics", "Leaderboard", "Reports"]
)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.subheader("Overview Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Students", len(df))
    c2.metric("Avg Marks", round(df["avg_marks"].mean(), 2))
    c3.metric("Attendance", round(df["attendance"].mean(), 2))
    c4.metric("Top Score", round(df["avg_marks"].max(), 2))

    st.plotly_chart(
        px.bar(df,
               x="name",
               y=["Maths", "Science", "English", "Social", "Computer"],
               barmode="group",
               color_discrete_sequence=px.colors.qualitative.Set2,
               title="Subject Wise Performance"),
        use_container_width=True
    )

    st.plotly_chart(
        px.pie(df,
               names="name",
               values="avg_marks",
               color_discrete_sequence=px.colors.sequential.RdBu,
               title="Student Performance Share"),
        use_container_width=True
    )

# =========================
# STUDENTS
# =========================
elif menu == "Students":

    st.subheader("Student Profiles")

    for s in df.to_dict("records"):

        with st.container():

            st.markdown(f"### {s['avatar']} {s['name']}")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Class:", s["class"])
                st.write("Attendance:", f"{s['attendance']}%")
                st.write("Blood:", s["blood_group"])
                st.write("Phone:", s["phone"])
                st.write("Parent:", s["parent_phone"])
                st.write("Address:", s["address"])

            with col2:
                st.write("Maths:", s["Maths"])
                st.write("Science:", s["Science"])
                st.write("English:", s["English"])
                st.write("Social:", s["Social"])
                st.write("Computer:", s["Computer"])

                st.progress(s["avg_marks"] / 100)
                st.write("Avg Marks:", round(s["avg_marks"], 2))

            st.divider()

# =========================
# ADD STUDENT
# =========================
elif menu == "Add Student":

    st.subheader("Add Student")

    name = st.text_input("Name")
    cls = st.text_input("Class")
    att = st.slider("Attendance", 0, 100, 80)

    maths = st.slider("Maths", 0, 100, 50)
    science = st.slider("Science", 0, 100, 50)
    english = st.slider("English", 0, 100, 50)
    social = st.slider("Social", 0, 100, 50)
    computer = st.slider("Computer", 0, 100, 50)

    blood = st.text_input("Blood Group")
    phone = st.text_input("Phone")
    parent_phone = st.text_input("Parent Phone")
    address = st.text_input("Address")
    avatar = st.selectbox("Avatar", ["👨‍🎓", "👩‍🎓", "🧑‍🎓"])

    if st.button("Add Student"):

        st.session_state.students.append({
            "id": len(st.session_state.students)+1,
            "name": name,
            "class": cls,
            "attendance": att,
            "blood_group": blood,
            "phone": phone,
            "parent_phone": parent_phone,
            "address": address,
            "avatar": avatar,
            "subjects": {
                "Maths": maths,
                "Science": science,
                "English": english,
                "Social": social,
                "Computer": computer
            }
        })

        st.success("Student Added 🚀")

# =========================
# ANALYTICS
# =========================
elif menu == "Analytics":

    st.subheader("Advanced Analytics Dashboard")

    st.plotly_chart(
        px.bar(df,
               x="name",
               y=["Maths", "Science", "English", "Social", "Computer"],
               barmode="group",
               color_discrete_sequence=px.colors.qualitative.Set3,
               title="Subject Comparison"),
        use_container_width=True
    )

    # ✅ UPDATED SCATTER CHART WITH STUDENT NAMES
    fig = px.scatter(
        df,
        x="attendance",
        y="avg_marks",
        size="avg_marks",
        color="avg_marks",
        text="name",
        color_continuous_scale="Viridis",
        title="Attendance vs Performance"
    )

    fig.update_traces(
        textposition="top center",
        marker=dict(
            line=dict(width=2, color="white")
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.plotly_chart(
        px.box(df,
               y=["Maths", "Science", "English", "Social", "Computer"],
               color_discrete_sequence=["#22c55e"],
               title="Subject Spread"),
        use_container_width=True
    )

    st.plotly_chart(
        px.histogram(df,
                     x="avg_marks",
                     nbins=10,
                     color_discrete_sequence=["#16a34a"],
                     title="Performance Distribution"),
        use_container_width=True
    )

    st.plotly_chart(
        px.pie(df,
               names="name",
               values="avg_marks",
               color_discrete_sequence=px.colors.sequential.Plasma,
               title="Contribution Share"),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(df.sort_values("avg_marks"),
                x="name",
                y="avg_marks",
                markers=True,
                color_discrete_sequence=["#22c55e"],
                title="Ranking Trend"),
        use_container_width=True
    )

# =========================
# LEADERBOARD
# =========================
elif menu == "Leaderboard":

    st.subheader("Top Students")

    st.dataframe(df.sort_values("avg_marks", ascending=False))

# =========================
# REPORTS
# =========================
elif menu == "Reports":

    st.subheader("📄 Student Report Card")

    selected = st.selectbox(
        "Select Student",
        df["name"].tolist()
    )

    student = df[df["name"] == selected].iloc[0]

    avg = round(student["avg_marks"], 2)

    if avg >= 90:
        grade = "A+"
        result = "Outstanding"
    elif avg >= 80:
        grade = "A"
        result = "Excellent"
    elif avg >= 70:
        grade = "B"
        result = "Very Good"
    elif avg >= 60:
        grade = "C"
        result = "Good"
    else:
        grade = "D"
        result = "Needs Improvement"

    st.markdown("""
    <style>

    .report-container{
        background:white;
        padding:35px;
        border-radius:15px;
        color:black;
        border:2px solid #ddd;
    }

    .school-title{
        text-align:center;
        color:#166534;
        font-size:34px;
        font-weight:bold;
    }

    .subtitle{
        text-align:center;
        color:gray;
        margin-bottom:25px;
    }

    .info-box{
        background:#f8fafc;
        padding:15px;
        border-radius:10px;
        border:1px solid #e5e7eb;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="report-container">
        <div class="school-title">
        EDUVISION INTERNATIONAL SCHOOL
        </div>

        <div class="subtitle">
        Academic Performance Report Card
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 👤 Student Information")

    c1,c2 = st.columns(2)

    with c1:
        st.write("**Name:**", student["name"])
        st.write("**Class:**", student["class"])
        st.write("**Blood Group:**", student["blood_group"])

    with c2:
        st.write("**Phone:**", student["phone"])
        st.write("**Attendance:**", f"{student['attendance']}%")
        st.write("**Address:**", student["address"])

    st.divider()

    st.markdown("### 📚 Academic Performance")

    marks_df = pd.DataFrame({
        "Subject":[
            "Maths",
            "Science",
            "English",
            "Social",
            "Computer"
        ],
        "Marks":[
            student["Maths"],
            student["Science"],
            student["English"],
            student["Social"],
            student["Computer"]
        ]
    })

    st.table(marks_df)

    st.divider()

    c1,c2,c3 = st.columns(3)

    c1.metric("Average", avg)
    c2.metric("Grade", grade)
    c3.metric("Result", result)

    st.divider()

    st.markdown("### 📝 Teacher's Remark")

    st.success(
        f"{student['name']} has shown {result.lower()} "
        f"academic performance throughout the term. "
        f"Attendance and classroom participation are satisfactory."
    )

    st.divider()

    col1,col2 = st.columns(2)

    with col1:
        st.write("")
        st.write("")
        st.write("____________________")
        st.write("Class Teacher")

    with col2:
        st.write("")
        st.write("")
        st.write("____________________")
        st.write("Principal")