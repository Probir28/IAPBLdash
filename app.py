import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="HR Insights Dashboard", layout="wide")

# Load datasets
@st.cache_data
def load_data():
    ea = pd.read_csv("EA.csv")
    happiness = pd.read_excel("Happiness Score Data.xlsx")
    return ea, happiness

ea, happiness = load_data()

# Sidebar filters
st.sidebar.header("Filter Employee Dataset")
selected_dept = st.sidebar.multiselect("Department", options=ea["Department"].unique(), default=ea["Department"].unique())
selected_job = st.sidebar.multiselect("Job Role", options=ea["JobRole"].unique(), default=ea["JobRole"].unique())
age_range = st.sidebar.slider("Age Range", int(ea["Age"].min()), int(ea["Age"].max()), (25, 45))

ea_filtered = ea[
    (ea["Department"].isin(selected_dept)) &
    (ea["JobRole"].isin(selected_job)) &
    (ea["Age"].between(age_range[0], age_range[1]))
]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Attrition Summary", "😊 Happiness Score Insights", "📈 Deep Analysis", "📌 Correlation & KPIs"])

# ---------------------- TAB 1 ---------------------
with tab1:
    st.header("Attrition Summary")
    st.markdown("**Overall Attrition Count**")
    fig1 = px.histogram(ea, x="Attrition", color="Attrition", title="Attrition Count")
    st.plotly_chart(fig1)

    st.markdown("**Attrition by Department**")
    fig2 = px.histogram(ea_filtered, x="Department", color="Attrition", barmode="group")
    st.plotly_chart(fig2)

    st.markdown("**Attrition by Job Role**")
    fig3 = px.histogram(ea_filtered, x="JobRole", color="Attrition", barmode="group")
    st.plotly_chart(fig3)

    st.markdown("**Attrition vs Age Distribution**")
    fig4 = px.histogram(ea_filtered, x="Age", color="Attrition", nbins=20)
    st.plotly_chart(fig4)

    st.markdown("**Monthly Income by Attrition**")
    fig5 = px.box(ea_filtered, x="Attrition", y="MonthlyIncome", color="Attrition")
    st.plotly_chart(fig5)

# ---------------------- TAB 2 ---------------------
with tab2:
    st.header("Happiness Score Insights")
    st.markdown("**Happiness Score by Region**")
    fig6 = px.box(happiness, x="Region", y="HappinessScore", points="all")
    st.plotly_chart(fig6)

    st.markdown("**GDP vs Happiness Score**")
    fig7 = px.scatter(happiness, x="GDP_PerCapita", y="HappinessScore", color="Region", hover_name="Country")
    st.plotly_chart(fig7)

    st.markdown("**Life Expectancy vs Happiness Score**")
    fig8 = px.scatter(happiness, x="HDI", y="HappinessScore", color="Region")
    st.plotly_chart(fig8)

    st.markdown("**Alcohol Consumption vs Happiness**")
    fig9 = px.scatter(happiness, x="Alcohol Consumption", y="HappinessScore", color="Region")
    st.plotly_chart(fig9)

# ---------------------- TAB 3 ---------------------
with tab3:
    st.header("Deep Dive Analysis")
    st.markdown("**Education Field vs Attrition**")
    fig10 = px.histogram(ea_filtered, x="EducationField", color="Attrition", barmode="group")
    st.plotly_chart(fig10)

    st.markdown("**Business Travel vs Attrition**")
    fig11 = px.histogram(ea_filtered, x="BusinessTravel", color="Attrition", barmode="group")
    st.plotly_chart(fig11)

    st.markdown("**Gender vs Attrition**")
    fig12 = px.histogram(ea_filtered, x="Gender", color="Attrition", barmode="group")
    st.plotly_chart(fig12)

    st.markdown("**Work Life Balance vs Attrition**")
    fig13 = px.box(ea_filtered, x="WorkLifeBalance", y="Age", color="Attrition")
    st.plotly_chart(fig13)

    st.markdown("**Distance From Home vs Attrition**")
    fig14 = px.histogram(ea_filtered, x="DistanceFromHome", color="Attrition")
    st.plotly_chart(fig14)

# ---------------------- TAB 4 ---------------------
with tab4:
    st.header("Correlations & KPIs")
    st.markdown("**Attrition Dataset Correlation Heatmap**")
    num_cols = ea.select_dtypes(include=["int64", "float64"]).drop(columns=["EmployeeCount", "StandardHours", "EmployeeNumber"])
    corr = num_cols.corr()
    fig15, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig15)

    st.markdown("**Happiness Score Correlation Heatmap**")
    happiness_corr = happiness.drop(columns=["Country", "Region"]).corr()
    fig16, ax2 = plt.subplots(figsize=(8, 6))
    sns.heatmap(happiness_corr, annot=True, cmap="YlGnBu", ax=ax2)
    st.pyplot(fig16)

    st.markdown("**KPI Snapshot**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", len(ea))
    col2.metric("Attrition Rate", f"{(ea['Attrition'] == 'Yes').mean() * 100:.2f}%")
    col3.metric("Avg Happiness", f"{happiness['HappinessScore'].mean():.2f}")
