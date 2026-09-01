import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load Data
# -------------------------------
uploaded_file = st.file_uploader("Upload the Tabulation Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    st.title("📊 First Year Student Dashboard")
    st.markdown("Interactive insights department-wise and class-wise")

    # -------------------------------
    # Overall Snapshot
    # -------------------------------
    st.header("Institute Snapshot")
    total_students = len(df)
    pass_count = (df['result'].str.upper() == "PASS").sum()
    fail_count = (df['result'].str.upper() == "FAIL").sum()
    avg_sgpa = df['sgpa'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Pass Count", pass_count)
    col3.metric("Average SGPA", f"{avg_sgpa:.2f}")

    # Pie chart Pass vs Fail
    fig_passfail = px.pie(
        names=["Pass", "Fail"],
        values=[pass_count, fail_count],
        title="Pass vs Fail Distribution"
    )
    st.plotly_chart(fig_passfail)

    # -------------------------------
    # Department-wise Insights
    # -------------------------------
    st.header("Department-wise Insights")
    dept_group = df.groupby("department").agg(
        avg_sgpa=("sgpa", "mean"),
        pass_count=("result", lambda x: (x.str.upper() == "PASS").sum()),
        total=("result", "count")
    )
    dept_group["pass_percentage"] = dept_group["pass_count"] / dept_group["total"] * 100

    st.dataframe(dept_group)

    fig_dept = px.bar(
        dept_group,
        x=dept_group.index,
        y="avg_sgpa",
        title="Average SGPA by Department",
        color="avg_sgpa",
        text_auto=True
    )
    st.plotly_chart(fig_dept)

    # -------------------------------
    # SGPA Distribution
    # -------------------------------
    st.header("SGPA Distribution")
    fig_hist = px.histogram(df, x="sgpa", nbins=20, title="SGPA Histogram")
    st.plotly_chart(fig_hist)

    fig_box = px.box(df, x="department", y="aggregate marks obtained", title="Aggregate Marks Spread by Department")
    st.plotly_chart(fig_box)

    # -------------------------------
    # Internal vs External Scatter
    # -------------------------------
    st.header("Internal vs External Performance")
    if "sub1 internal" in df.columns and "sub1 external" in df.columns:
        fig_scatter = px.scatter(
            df,
            x="sub1 internal",
            y="sub1 external",
            color="department",
            title="Internal vs External Marks (Subject 1)"
        )
        st.plotly_chart(fig_scatter)

    # -------------------------------
    # Student Lookup
    # -------------------------------
    st.header("Student Performance Lookup")
    student_name = st.text_input("Enter Student Name")
    if student_name:
        student_data = df[df['name of candidate'].str.contains(student_name, case=False, na=False)]
        st.write(student_data)

    # -------------------------------
    # Export Dashboard
    # -------------------------------
    st.header("Export Dashboard")
    st.markdown("You can save this dashboard as an HTML file using the command below in terminal:")
    st.code("streamlit run fy_dashboard.py --server.headless true --server.fileWatcherType none")

