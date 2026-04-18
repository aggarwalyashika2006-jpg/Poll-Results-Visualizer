import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Poll Analytics Dashboard", layout="wide")
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: bold;
    color: #2E86C1;
}
.section {
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="main-title">📊 Poll Analytics Dashboard</p>', unsafe_allow_html=True)
st.write("Interactive Insights from Survey Data")

# -----------------------
# LOAD DATA
# -----------------------
with st.spinner("Loading data..."):
    df = pd.read_csv("data/poll_data.csv")

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

age = st.sidebar.multiselect(
    "Select Age Group",
    options=df["Age_Group"].unique(),
    default=df["Age_Group"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Apply filters
df = df[
    (df["Region"].isin(region)) &
    (df["Age_Group"].isin(age)) &
    (df["Gender"].isin(gender))
]

# -----------------------
# PREPARE DATA
# -----------------------
vote_counts = df["Choice"].value_counts()

region_data = pd.crosstab(df["Region"], df["Choice"])
gender_data = pd.crosstab(df["Gender"], df["Choice"])

df["Date"] = pd.to_datetime(df["Date"])
trend = df.groupby("Date")["Choice"].value_counts().unstack().fillna(0)

# -----------------------
# KPI METRICS
# -----------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Responses", len(df))
col2.metric("Top Choice", vote_counts.idxmax())
col3.metric("Highest Votes", vote_counts.max())

# -----------------------
# VISUALIZATIONS
# -----------------------
st.subheader("📊 Visualizations")

col1, col2 = st.columns(2)

# Bar Chart
with col1:
    fig, ax = plt.subplots(figsize=(4,3))
    vote_counts.sort_values().plot(kind='bar', ax=ax)
    ax.set_title("Vote Distribution")
    ax.set_ylabel("Votes")
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

# Pie Chart
with col2:
    fig2, ax2 = plt.subplots(figsize=(4,3))
    vote_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    ax2.set_ylabel("")
    ax2.set_title("Vote Share")
    plt.tight_layout()
    st.pyplot(fig2, use_container_width=False)

# -----------------------
# REGION ANALYSIS
# -----------------------
st.subheader("🌍 Region-wise Analysis")

st.dataframe(region_data)

fig3, ax3 = plt.subplots(figsize=(5,3))
region_data.plot(kind='bar', stacked=True, ax=ax3)
plt.tight_layout()
st.pyplot(fig3, use_container_width=False)

# -----------------------
# GENDER ANALYSIS (NEW)
# -----------------------
st.subheader("👥 Gender-wise Analysis")

st.dataframe(gender_data)

fig4, ax4 = plt.subplots(figsize=(5,3))
gender_data.plot(kind='bar', stacked=True, ax=ax4)
plt.tight_layout()
st.pyplot(fig4, use_container_width=False)

# -----------------------
# TREND ANALYSIS
# -----------------------
st.subheader("📈 Trend Over Time")

fig5, ax5 = plt.subplots(figsize=(6,3))
trend.plot(ax=ax5)
plt.tight_layout()
st.pyplot(fig5, use_container_width=False)

# -----------------------
# DOWNLOAD DATA
# -----------------------
st.subheader("⬇️ Download Data")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv'
)
st.subheader("🔍 Explore Specific Product")

selected_choice = st.selectbox("Select Product", df["Choice"].unique())

filtered_data = df[df["Choice"] == selected_choice]

st.write(f"Showing data for {selected_choice}")
st.dataframe(filtered_data.head(10))

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("🧠 Insights")

top = vote_counts.idxmax()
percent = (vote_counts.max() / len(df)) * 100
st.subheader("📌 Key Insights")

top_choice = vote_counts.idxmax()
percentage = (vote_counts.max() / len(df)) * 100

top_region = df["Region"].value_counts().idxmax()

st.success(f"{top_choice} is leading with {percentage:.2f}% votes.")
st.info(f"Most active region: {top_region}")

st.success(f"{top} is leading with {percent:.2f}% votes.")
