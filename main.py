import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Risk Assessment Dashboard",
    layout="wide"
)

# Data
data = {
    'Asset': ['Electronic Data', 'Electronic Data', 'Revenue Management System', 
              'Revenue Management System', 'IT Hardware', 'Reputation', 'Staff'],
    'Vulnerability': ['Human Error', 'SQL Injection', 'Cross-Site Scripting', 
                     'Denial of Services', 'Power Interruptions', 'Data Breach', 'Social Engineering'],
    'Asset_Value': [5, 5 ,3 ,3 ,2 ,5 ,2],  # Updated values
    'Exposure_Factor': [8,8,7,6,9,6,9],
    'Base_Value': ['1,000,000','1,000,000','100,000 to 500,000','100,000 to 500,000','10,000 to 100,000','1,000,000','10,000 to 100,000',],
    'ALE': ['12,000,000','12,000,000','400,000 to 2,000,000','100,000 to 500,000','480,000 to 4,800,000','1,000,000','480,000 to 4,800,000'],
    'ARO_Description': ['Monthly','Monthly','Quarterly','Annually','Weekly','Annually','Weekly'],
    'Justification': ['Top risk from mental stress and physical fatigue',
                     'Requires firewall and intrusion prevention',
                     'Needs Data Leakage Prevention systems',
                     'Caused by low memory and bandwidth limitations',
                     'Requires backup power generators',
                     'Significant impact on organizational value',
                     'Mitigated through security awareness training']
}

df = pd.DataFrame(data)

# Title and description
st.title("Risk Assessment Dashboard")
st.markdown("### Overview of Security Risks and Their Financial Impact")

# Metrics - Key Statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Annual Loss Expectancy", f"£{df['ALE'].sum():,.0f}")
with col2:
    st.metric("Highest Single Loss", f"£{df['ALE'].max():,.0f}")
with col3:
    st.metric("Number of Risk Factors", len(df))

# Create two columns for the layout
left_column, right_column = st.columns([2, 1])

with left_column:
    # ALE by Asset Type
    fig_ale = px.bar(
        df,
        x='Asset',
        y='ALE',
        color='Vulnerability',
        title='Annual Loss Expectancy by Asset Type',
        labels={'ALE': 'Annual Loss Expectancy (£)'},
        hover_data=['ARO_Description', 'Justification']
    )
    fig_ale.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_ale, use_container_width=True)

    # Risk Matrix
    fig_matrix = go.Figure()
    fig_matrix.add_trace(go.Scatter(
        x=df['Exposure_Factor'],
        y=df['Asset_Value'],
        mode='markers+text',
        marker=dict(
            size=df['ALE'] / 1000000,  # Size proportional to ALE
            sizemode='area',
            sizeref=0.1,
            color=df['ARO'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Annual Rate of Occurrence')
        ),
        text=df['Vulnerability'],
        textposition="top center",
        hovertemplate="<b>%{text}</b><br>" +
                      "Exposure Factor: %{x}<br>" +
                      "Asset Value: %{y}<br>" +
                      "<extra></extra>"
    ))
    fig_matrix.update_layout(
        title='Risk Matrix (Bubble size represents ALE)',
        xaxis_title='Exposure Factor',
        yaxis_title='Asset Value',
        showlegend=False
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

with right_column:
    # Risk Details Table
    st.subheader("Risk Details")
    st.dataframe(
        df[['Asset', 'Vulnerability', 'ARO_Description', 'ALE', 'Justification']]
        .sort_values('ALE', ascending=False)
        .style.format({'ALE': '£{:,.0f}'})
    )

    # Filters for detailed analysis
    st.subheader("Risk Analysis Filters")
    selected_asset = st.selectbox("Select Asset", options=['All'] + list(df['Asset'].unique()))
    
    if selected_asset != 'All':
        filtered_df = df[df['Asset'] == selected_asset]
    else:
        filtered_df = df
        
    # Show filtered details
    st.markdown("### Filtered Risk Details")
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['Asset']} - {row['Vulnerability']}"):
            st.write(f"**Base Value:** £{row['Base_Value']:,.0f}")
            st.write(f"**Exposure Factor:** {row['Exposure_Factor']:.1%}")
            st.write(f"**Annual Rate:** {row['ARO']} ({row['ARO_Description']})")
            st.write(f"**Annual Loss Expectancy:** £{row['ALE']:,.0f}")
            st.write(f"**Justification:** {row['Justification']}")

# Add a footer with timestamp
st.markdown("---")
st.markdown("*Dashboard last updated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S") + "*")