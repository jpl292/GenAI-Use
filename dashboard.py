
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Diary Study Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Merged_Weekly_AI_Diary_All_Personas.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter by")
selected_roles = st.sidebar.multiselect("Choose roles", options=df["Role"].unique(), default=df["Role"].unique())
filtered_df = df[df["Role"].isin(selected_roles)]

# Main KPIs
st.title("Generative AI Diary Study Dashboard")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Satisfaction", round(filtered_df["Satisfaction"].mean(), 2))
with col2:
    st.metric("Most Common Trust Level", filtered_df["Trust"].mode()[0])
with col3:
    st.metric("Most Common Familiarity Level", filtered_df["Familiarity"].mode()[0])

# Weekly Trend Line
st.subheader("Weekly Satisfaction Trend")
satisfaction_trend = filtered_df.groupby(["Week", "Role"]).agg({"Satisfaction": "mean"}).reset_index()
sns.lineplot(data=satisfaction_trend, x="Week", y="Satisfaction", hue="Role")
st.pyplot(plt.gcf())
plt.clf()

# AI Dependency Metrics
st.subheader("AI Dependency Indicators")
dep_columns = ["AI Manual Use", "Avoided Difficulty", "Avoided Growth", "Job Without AI", "Unnecessary Use"]
st.dataframe(filtered_df[dep_columns + ["Name", "Role", "Week"]].groupby("Role").mean().round(2))

# Work Quality & Social Impact
st.subheader("Work Quality and Social Impact")
col4, col5 = st.columns(2)

with col4:
    st.bar_chart(filtered_df.groupby("Work Quality Compared to Pre-AI").size())
with col5:
    st.bar_chart(filtered_df.groupby("Socialized Compared to Last Week").size())

# Connection Metrics
st.subheader("Social Connection Metrics")
connection_cols = ["Sense of Connection", "Acquaintance Impact", "Friend Impact", "Family Impact"]
st.dataframe(filtered_df[connection_cols + ["Name", "Role", "Week"]].groupby("Role").agg(lambda x: x.mode()[0] if x.dtype == 'O' else x.mean().round(2)))

# Mental & Emotional Self Report
st.subheader("Confidence & Creativity Self Report")
col6, col7 = st.columns(2)

with col6:
    st.bar_chart(filtered_df.groupby("Confidence Without AI").size())
with col7:
    st.bar_chart(filtered_df.groupby("Reduced Creativity").size())
