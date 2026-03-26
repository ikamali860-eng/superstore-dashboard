#!/usr/bin/env python
# coding: utf-8

# In[3]:


state_codes = {
    "Alabama":"AL", "Arizona":"AZ", "Arkansas":"AR",
    "California":"CA", "Colorado":"CO", "Connecticut":"CT", 
    "Delaware":"DE", "Florida":"FL", "Georgia":'GA', "Idaho":"ID",
    "Illinois":"IL", "Indiana":"IN", "Iowa":"IA", "Kansas":"KS",
    "Kentucky":"KY", "Louisiana":"LA", "Maine":"ME", "Maryland":"MD",
    "Massachusetts":"MA", "Michigan":"MI", "Minnesota":"MN", "Mississippi":"MS",
    "Missouri":"MO", "Montana":"MT", "Nebraska":"NE", "Nevada":"NV",
    "New Hampshire":"NH", "New Jersey":"NJ", "New Mexico":"NM", "New York":"NY",
    "North Carolina":"NC", "North Dakota":"ND", "Ohio":"OH", "Oklahoma":"OK",
    "Oregon":"OR", "Pennsylvania":"PA", "Rhode Island":"RI", "South Carolina":"SC",
    "South Dakota":"SD", "Tennessee":"TN", "Texas":"TX", "Utah":"UT", "Vermont":"VT",
    "Virginia":"VA", "Washington":"WA", "West Virginia":"WV", "Wisconsin":"WI",
    "Wyoming":"WY"
}


# In[4]:


import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
df = pd.read_excel('Superstore.xlsx')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['State Code'] = df['State'].map(state_codes)
st.title('Superstore Sales Dashboard')
st.sidebar.header('Filters')
region = st.sidebar.selectbox('Select Region', ['All'] + list(df['Region'].unique())) 
date_range = st.sidebar.date_input('Select Date Range', [df['Order Date'].min(), df['Order Date'].max()])
start_date, end_date = date_range
filtered = df[(df['Order Date'] >= pd.to_datetime(start_date)) & (df['Order Date'] <= pd.to_datetime(end_date))]
if region!= 'All':
    filtered = filtered[filtered['Region']==region]
filtered['Month'] = filtered['Order Date'].dt.month
total_sales = filtered['Sales'].sum()
total_orders = filtered['Order Date'].nunique()
avg_sales = filtered['Sales'].mean()
col1, col2, col3 = st.columns(3)
col1.metric('Total Sales', f'${total_sales:,.0f}')
col2.metric('Total Orders', total_orders)
col3.metric('Average Sale', f'${avg_sales:,.2f}')
sales_cat = filtered.groupby('Category')['Sales'].sum().reset_index()
sales_time = filtered.groupby('Order Date')['Sales'].sum().reset_index()
sales_region = filtered.groupby('Region')['Sales'].sum().reset_index()
top_products = filtered.groupby('Product Name')['Sales'].sum().reset_index().sort_values('Sales', ascending=False).head(10)
sales_state = filtered.groupby('State Code')['Sales'].sum().reset_index()
segment_sales = filtered.groupby('Segment')['Sales'].sum().reset_index()
heatmap_data = filtered.groupby(['Month', 'Category'])['Sales'].sum().reset_index()
monthly_sales = filtered.groupby(['Month'])['Sales'].sum().reset_index()
pareto = filtered.groupby('Product Name')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
pareto['Cumulative Sales'] = pareto['Sales'].cumsum()
pareto['Cumulative %'] = 100 * pareto['Cumulative Sales'] / pareto['Sales'].sum()
pareto = pareto.head(15)
fig1 = px.bar(
    sales_cat,
    x='Category',
    y='Sales',
    color='Category',
    title='Sales by Category'
)
fig2 = px.line(
    sales_time,
    x='Order Date',
    y='Sales',
    title='Sales Over Time'
)
fig3 = px.pie(
    sales_region,
    names='Region',
    values='Sales',
    title='Sales by Region'
)
fig4 = px.bar(
    top_products,
    x='Sales',
    y='Product Name',
    orientation='h',
    title='Top 10 Products'
)
fig5 = px.choropleth(
    sales_state,
    locations='State Code',
    locationmode='USA-states',
    color='Sales',
    scope='usa',
    title='Sales by State'
)
fig_segment = px.bar(
    segment_sales,
    x="Segment",
    y="Sales",
    color="Segment",
    title="Sales by Customer Segment"
)
fig_heatmap = px.density_heatmap(
    heatmap_data,
    x='Month',
    y='Category',
    z='Sales',
    color_continuous_scale='Blues',
    title='Sales Heatmap'
)
fig_month = px.line(
    monthly_sales,
    x='Month',
    y='Sales',
    markers=True,
    title='Monthly Sales Trend'
)
fig_pareto = go.Figure()
fig_pareto.add_bar(
    x=pareto['Product Name'],
    y=pareto['Sales'],
    name='Sales'
)
fig_pareto.add_scatter(
    x=pareto['Product Name'],
    y=pareto['Cumulative %'],
    name='Cumulative %',
    yaxis='y2',
    mode='lines+markers'
)
fig_pareto.update_layout(
    title='Pareto Analysis - Product Sales',
    yaxis=dict(title='Sales'),
    yaxis2=dict(title='Cumulative %',
                overlaying='y',
                side='right'
               )
)
col4, col5 = st.columns(2)
col4.plotly_chart(fig1, use_container_width=True)
col5.plotly_chart(fig2, use_container_width=True)
col6, col7 = st.columns(2)
col6.plotly_chart(fig3, use_container_width=True)
col7.plotly_chart(fig4, use_container_width=True)
col8, = st.columns(1)
col8.plotly_chart(fig5, use_container_width=True)
col9, col10 = st.columns(2)
col9.plotly_chart(fig_segment, use_container_width=True)
col10.plotly_chart(fig_heatmap, use_container_width=True)
st.plotly_chart(fig_month, use_container_width=True)
st.plotly_chart(fig_pareto, use_container_width=True)

