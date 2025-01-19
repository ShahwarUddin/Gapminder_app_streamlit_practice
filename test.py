import streamlit as st
import pandas as pd
import plotly.express as px

# Load Gapminder dataset



df = px.data.gapminder()

# Configure the page
st.set_page_config(page_title="Gapminder Dashboard", 
                   page_icon="🌍", 
                   layout="wide", 
                   initial_sidebar_state="expanded")

# Sidebar
st.sidebar.title("🌍 Dashboard Controls")
selected_year = st.sidebar.slider("Select Year", min_value=int(df['year'].min()), 
                                   max_value=int(df['year'].max()), step=5, value=2007)
selected_continent = st.sidebar.multiselect(
    "Select Continent(s)", options=df['continent'].unique(), default=df['continent'].unique()
)
st.sidebar.write("### Metrics Filters")
population_filter = st.sidebar.slider("Filter by Population", 
                                       min_value=int(df['pop'].min()), 
                                       max_value=int(df['pop'].max()), 
                                       value=(int(df['pop'].min()), int(df['pop'].max())))

# Filter data
filtered_df = df[(df['year'] == selected_year) & 
                 (df['continent'].isin(selected_continent)) & 
                 (df['pop'].between(population_filter[0], population_filter[1]))]

# Main Layout
st.title("🌍 Gapminder Dashboard")
st.markdown(f"### Year: {selected_year}")
st.markdown("---")

# Row 1: Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Countries", len(filtered_df['country'].unique()))
col2.metric("Total Population", f"{filtered_df['pop'].sum() / 1e9:.2f} Billion")
col3.metric("Average Life Expectancy", f"{filtered_df['lifeExp'].mean():.2f} years")
col4.metric("Average GDP per Capita", f"${filtered_df['gdpPercap'].mean():,.2f}")

st.markdown("---")

# Row 2: Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 GDP per Capita vs Life Expectancy")
    scatter_fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", size="pop", 
                              color="continent", hover_name="country", 
                              log_x=True, size_max=60, 
                              title="GDP vs Life Expectancy (Bubble Chart)")
    st.plotly_chart(scatter_fig, use_container_width=True)

with col2:
    st.subheader("🌍 Population by Continent")
    bar_fig = px.bar(filtered_df.groupby("continent")["pop"].sum().reset_index(), 
                     x="continent", y="pop", 
                     color="continent", title="Total Population by Continent")
    st.plotly_chart(bar_fig, use_container_width=True)

# Row 3: DataFrame
st.subheader("📋 Filtered Data")
# st.dataframe(filtered_df)

# Display the dataframe with progress bars
st.subheader("📋 Filtered Data with Population Progress Bars")
st.dataframe(
    filtered_df,
    column_order=["country", "pop", "lifeExp", "gdpPercap"],
    hide_index=True,
    column_config={
        "country": st.column_config.TextColumn("Country"),
        "pop": st.column_config.ProgressColumn(
            "Population",
            format="%d",
            min_value=0,
            max_value=int(df["pop"].max()),
        ),
        "lifeExp": st.column_config.NumberColumn("Life Expectancy", format="%.2f"),
        "gdpPercap": st.column_config.NumberColumn("GDP per Capita", format="$%.2f"),
    },
    use_container_width=True,
)

st.markdown("---")

# Row 4: Pie Chart
st.subheader("🌍 Population Distribution")
pie_fig = px.pie(filtered_df, values="pop", names="continent", 
                 title="Population Distribution by Continent")
st.plotly_chart(pie_fig, use_container_width=True)

# Footer
st.markdown("### Built with Streamlit and Plotly | Gapminder Dashboard")
