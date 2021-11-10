import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.set_page_config(page_title = "Suicides in India")

df = pd.read_excel("cause-of-suicide-Table 2.5 state-ut-city.xlsx", sheet_name = "Sheet1")

df['Total'] = df['Male'] + df['Female']

india = gpd.read_file("./India_State_Boundary.shp")

india.replace({
    "Andaman & Nicobar": "A&N Islands",
    "Jammu and Kashmir": "Jammu & Kashmir",
    "Telengana": "Telangana",
    "Tamilnadu": "Tamil Nadu",
    "Chhattishgarh": "Chhattisgarh",
    "Daman and Diu and Dadra and Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu"
}, inplace = True)

india.rename(columns = {
    "Name": "State"
}, inplace = True)

india['State'] = india['State'].str.title()
df['State'] = df['State'].str.title()
states = sorted(set(df['State']))
causes = sorted(set(df['Cause']))

geo_df = india.merge(df, on = "State").set_index("State")

# states = sorted(set(geo_df['State']))
# causes = sorted(set(geo_df['Cause']))

with st.sidebar:
    st.title("India Suicides Data 2020")

    choice = st.radio("Select one", ["All India", "State-wise Causes", "Causes Choropleth Map"])

    st.write("Source: India Suicide Data 2020, National Crime Records Bureau, Government of India")

if choice == "All India":
    st.header("All India Level")

    top_10_states = df.groupby('State')['Total'].sum().nlargest(10).sort_values(ascending = True)
    top_10_states_fig = px.bar(
        top_10_states,
        orientation = 'h',
        title = 'Top 10 States with Suicides in India in 2020',
        labels = {
            "value": "Total Cases",
            "variable": "Total Cases"
        }
    )
    st.plotly_chart(top_10_states_fig)

    top_10_causes = df.groupby('Cause')['Total'].sum().nlargest(10).sort_values(ascending = True)
    top_10_causes_fig = px.bar(
        top_10_causes,
        orientation = 'h',
        title = 'Top Causes of Suicides in India in 2020',
        labels = {
            "value": "Total Cases",
            "variable": "Total Cases"
        }
    )
    st.plotly_chart(top_10_causes_fig)

    top_10_causes_female = df.groupby('Cause')['Female'].sum().nlargest(10).sort_values(ascending = True)
    top_10_causes_female_fig = px.bar(
        top_10_causes_female,
        orientation = 'h',
        title = 'Top Causes of Suicides for Females in India in 2020',
        labels = {
            "value": "Total Cases",
            "variable": "Total Cases"
        }
    )
    st.plotly_chart(top_10_causes_female_fig)

    top_10_causes_male = df.groupby('Cause')['Male'].sum().nlargest(10).sort_values(ascending = True)
    top_10_causes_male_fig = px.bar(
        top_10_causes_male,
        orientation = 'h',
        title = 'Top Causes of Suicides for Males in India in 2020',
        labels = {
            "value": "Total Cases",
            "variable": "Total Cases"
        }
    )
    st.plotly_chart(top_10_causes_male_fig)

elif choice == "State-wise Causes":
    state = st.sidebar.selectbox('Select State', states)
    df = df[df['State'] == state].sort_values('Total', ascending = False)

    top_10_causes = df.groupby('Cause')['Total'].sum().nlargest(10).sort_values(ascending = True)
    top_10_causes_fig = px.bar(
        top_10_causes,
        orientation = 'h',
        title = f'Top Causes of Suicides in {state} in 2020',
        labels = {
            "value": "Total Cases",
            "variable": "Total Cases"
        }
    )
    st.plotly_chart(top_10_causes_fig)

    top_10_causes_female = df.groupby('Cause')['Female'].sum().nlargest(10).sort_values(ascending = True)
    top_10_causes_female_fig = px.bar(
        top_10_causes_female,
        orientation = 'h',
        title = f'Top Causes of Suicides for Females in {state} in 2020',
        labels = {
            "value": "Total Cases",
            "variable": "Total Cases"
        }
    )
    st.plotly_chart(top_10_causes_female_fig)

    top_10_causes_male = df.groupby('Cause')['Male'].sum().nlargest(10).sort_values(ascending = True)
    top_10_causes_male_fig = px.bar(
        top_10_causes_male,
        orientation = 'h',
        title = f'Top Causes of Suicides for Males in {state} in 2020',
        labels = {
            "value": "Total Cases",
            "variable": "Total Cases"
        }
    )
    st.plotly_chart(top_10_causes_male_fig)

else:
    cause = st.sidebar.selectbox('Select Cause', causes)

    cdf = geo_df[geo_df['Cause'] == cause]

    cause_fig = px.choropleth(
        cdf,
        geojson = cdf.geometry,
        locations = cdf.index,
        color = "Total",
        projection = 'mercator',
        height = 600,
        width = 600
    )

    cause_fig.update_geos(fitbounds = "locations", visible=True)
    st.subheader(f"Chart showing the number of suicides due to {cause}")
    st.plotly_chart(cause_fig, use_container_width=True)
