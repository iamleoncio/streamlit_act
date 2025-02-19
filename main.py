import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Offshore Data 🌍")

col1, col2, col3 = st.columns([1, 3, 1])

data = pd.read_csv("CAPSTONEDATA.csv")
data["GROSSSALES"] = pd.to_numeric(data["GROSSSALES"], errors="coerce")

summary = data.groupby("COUNTRY")["GROSSSALES"].sum().reset_index()
summary["GROSSSALES"] = summary["GROSSSALES"].apply(lambda x: f"${x:,.2f}")

country_coords = {
    "United States": (37.0902, -95.7129),
    "Canada": (56.1304, -106.3468),
    "United Kingdom": (55.3781, -3.4360),
    "Germany": (51.1657, 10.4515),
    "France": (46.6034, 1.8883),
    "India": (20.5937, 78.9629),
    "China": (35.8617, 104.1954),
    "Japan": (36.2048, 138.2529),
    "Australia": (-25.2744, 133.7751),
    "Brazil": (-14.2350, -51.9253)
}

summary["latitude"] = summary["COUNTRY"].map(lambda x: country_coords.get(x, (None, None))[0])
summary["longitude"] = summary["COUNTRY"].map(lambda x: country_coords.get(x, (None, None))[1])
map_data = summary.dropna(subset=["latitude", "longitude"])

with col1:
    st.subheader("📊 Gross Sales by Country")
    st.markdown("---")

    selected_country = st.selectbox("🌎 Select a Country", ["All"] + list(summary["COUNTRY"].unique()))

    if selected_country != "All":
        filtered_summary = summary[summary["COUNTRY"] == selected_country]
    else:
        filtered_summary = summary

    st.dataframe(filtered_summary[["COUNTRY", "GROSSSALES"]], use_container_width=True)

    csv_data = summary.to_csv(index=False).encode("utf-8")
    st.download_button(label="⬇️ Download Summary Data", data=csv_data, file_name="summary_data.csv", mime="text/csv")

with col2:
    st.subheader("💰 GROSS SALES")
    st.markdown("---")
    metric1, metric2, metric3 = st.columns(3)
    with metric1:
        st.metric(label="📈 Total Sales", value=f"${data['GROSSSALES'].sum():,.2f}")

    with metric2:
        st.metric(label="📉 Average Sales", value=f"${data['GROSSSALES'].mean():,.2f}")

    with metric3:
        st.metric(label="🏆 Max Sale", value=f"${data['GROSSSALES'].max():,.2f}")

    st.subheader("📦 Gross Sales by Category")
    st.markdown("---")
    category_by_gross = data.groupby("CATEGORY")["GROSSSALES"].sum().reset_index()
    st.bar_chart(category_by_gross, x="CATEGORY", y="GROSSSALES")

with col3:
    st.subheader("🗺️ Sales Distribution Map")
    st.markdown("---")
    st.map(map_data.rename(columns={"latitude": "lat", "longitude": "lon"}))

    st.header("💬 Chat with us!")
    st.markdown("---")
    if prompt := st.chat_input("Say something about us!" ):
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write(f"Echo: {prompt}")

st.markdown("---")
st.text("Made by Leon")
