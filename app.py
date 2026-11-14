import pandas as pd
import streamlit as st
import plotly.express as px
from db import run_query

st.set_page_config(page_title="Titanic Dashboard", page_icon="🚢", layout="wide")

st.title("🚢 Titanic Passenger Analysis Dashboard")

df = run_query("""
    SELECT *
    FROM titanic_project.passengers;
""")

st.set_page_config(
    page_title="Titanic Dashboard",
    page_icon="🚢",
    layout="wide"
)

# Top connection message
st.success("✅ Dashboard Connected Successfully")


# Sidebar filters
st.sidebar.header("Dashboard Filters")

genders = st.sidebar.multiselect(
    "Select Gender",
    options=df["sex"].dropna().unique(),
    default=df["sex"].dropna().unique().tolist()
)

classes = st.sidebar.multiselect(
    "Select Passenger Class",
    options=sorted(df["pclass"].dropna().unique()),
    default=sorted(df["pclass"].dropna().unique())
)

filtered_df = df[
    (df["sex"].isin(genders)) &
    (df["pclass"].isin(classes))
]

# KPI metrics
total = len(filtered_df)
survived = int(filtered_df["survived"].sum())
deaths = total - survived
rate = survived / total * 100 if total else 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Passengers", total)
c2.metric("Survived", survived)
c3.metric("Deaths", deaths)
c4.metric("Survival Rate", f"{rate:.2f}%")

st.divider()

# Chart 1: Survival distribution
st.subheader("1. Survival Distribution")

survival = filtered_df["survived"].value_counts().reset_index()
survival.columns = ["Survival", "Passengers"]
survival["Survival"] = survival["Survival"].map(
    {0: "Died", 1: "Survived"}
)

fig1 = px.pie(
    survival,
    names="Survival",
    values="Passengers",
    title="Survived vs Died",
    hole=0.4
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Gender analysis
st.subheader("2. Survival by Gender")

gender_data = filtered_df.groupby(
    ["sex", "survived"]
).size().reset_index(name="Passengers")

gender_data["Status"] = gender_data["survived"].map(
    {0: "Died", 1: "Survived"}
)

fig2 = px.bar(
    gender_data,
    x="sex",
    y="Passengers",
    color="Status",
    barmode="group",
    title="Gender-wise Survival"
)

st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Passenger class
st.subheader("3. Survival by Passenger Class")

class_data = filtered_df.groupby(
    ["pclass", "survived"]
).size().reset_index(name="Passengers")

class_data["Status"] = class_data["survived"].map(
    {0: "Died", 1: "Survived"}
)

fig3 = px.bar(
    class_data,
    x="pclass",
    y="Passengers",
    color="Status",
    barmode="group",
    title="Passenger Class vs Survival"
)

st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Age distribution
st.subheader("4. Age Distribution")

fig4 = px.histogram(
    filtered_df.dropna(subset=["age"]),
    x="age",
    nbins=30,
    title="Passenger Age Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Fare analysis
st.subheader("5. Average Fare by Class")

fare_data = filtered_df.groupby(
    "pclass"
)["fare"].mean().reset_index()

fig5 = px.bar(
    fare_data,
    x="pclass",
    y="fare",
    title="Average Ticket Fare by Passenger Class",
    labels={"pclass": "Passenger Class", "fare": "Average Fare"}
)

st.plotly_chart(fig5, use_container_width=True)

# Chart 6: Embarkation analysis
st.subheader("6. Passengers by Embarkation Port")

embark_data = filtered_df.groupby(
    "embarked"
).size().reset_index(name="Passengers")

fig6 = px.bar(
    embark_data,
    x="embarked",
    y="Passengers",
    title="Passengers from Each Port"
)

st.plotly_chart(fig6, use_container_width=True)

# Passenger records
st.subheader("7. Passenger Details")

st.dataframe(filtered_df, use_container_width=True)


# Chart 7: Survival by Age Group
st.subheader("7. Survival by Age Group")

age_data = filtered_df.dropna(subset=["age"]).copy()

age_data["age_group"] = pd.cut(
    age_data["age"],
    bins=[0, 18, 35, 60, 100],
    labels=["Child", "Young Adult", "Adult", "Senior"],
    include_lowest=True
)

age_survival = age_data.groupby(
    ["age_group", "survived"], observed=False
).size().reset_index(name="Passengers")

age_survival["Status"] = age_survival["survived"].map(
    {0: "Died", 1: "Survived"}
)

fig7 = px.bar(
    age_survival,
    x="age_group",
    y="Passengers",
    color="Status",
    barmode="group",
    title="Survival by Age Group"
)

st.plotly_chart(fig7, use_container_width=True)

# Chart 8: Family Size Analysis
st.subheader("8. Survival by Family Size")

family_data = filtered_df.copy()

family_data["family_size"] = (
    family_data["sibsp"] + family_data["parch"] + 1
)

family_survival = family_data.groupby(
    ["family_size", "survived"]
).size().reset_index(name="Passengers")

family_survival["Status"] = family_survival["survived"].map(
    {0: "Died", 1: "Survived"}
)

fig8 = px.bar(
    family_survival,
    x="family_size",
    y="Passengers",
    color="Status",
    barmode="group",
    title="Family Size vs Survival"
)

st.plotly_chart(fig8, use_container_width=True)

# Download filtered passenger data
st.subheader("9. Download Passenger Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Passenger Data (CSV)",
    data=csv,
    file_name="titanic_passengers.csv",
    mime="text/csv"
)
st.divider()

# Bottom connection message
st.success("✅ Dashboard Connected Successfully")