import streamlit as st
import pandas as pd
from data_generator import (generate_remittance_data, generate_mobile_money_data,
                          generate_purchase_history, generate_user_profile,
                          generate_real_time_transaction)
from credit_scoring import (calculate_remittance_score, calculate_mobile_money_score,
                          calculate_purchase_score, calculate_overall_score,
                          get_risk_category)
from visualization import (create_score_gauge, create_transaction_history,
                         create_category_distribution, create_risk_factors_radar,
                         create_real_time_monitor, create_transaction_monitoring_table)
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="BNPL Credit Scoring System", layout="wide")

# Initialize session state for real-time monitoring
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'score_history' not in st.session_state:
    st.session_state.score_history = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Title and description
st.title("BNPL Credit Scoring Dashboard")
st.markdown("""
This dashboard provides a comprehensive credit scoring analysis based on:
- Remittance History
- Mobile Money Usage
- Purchase History
""")

# Generate mock data
@st.cache_data
def load_data():
    user = generate_user_profile()
    remittance = generate_remittance_data()
    mobile_money = generate_mobile_money_data()
    purchases = generate_purchase_history()
    return user, remittance, mobile_money, purchases

user, remittance_data, mobile_money_data, purchase_data = load_data()

# Real-time Monitoring Section
st.header("Real-time Monitoring")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Generate New Transaction"):
        new_transaction = generate_real_time_transaction()
        st.session_state.transactions.append(new_transaction)

        # Recalculate scores
        current_score = calculate_overall_score(
            calculate_remittance_score(remittance_data),
            calculate_mobile_money_score(mobile_money_data),
            calculate_purchase_score(purchase_data)
        )

        st.session_state.score_history.append({
            'timestamp': datetime.now(),
            'score': current_score
        })

with col2:
    st.write(f"Last Update: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

with col3:
    auto_refresh = st.checkbox("Enable Auto-refresh (5s)", value=False)

if auto_refresh:
    time_diff = (datetime.now() - st.session_state.last_update).total_seconds()
    if time_diff >= 5:
        new_transaction = generate_real_time_transaction()
        st.session_state.transactions.append(new_transaction)

        current_score = calculate_overall_score(
            calculate_remittance_score(remittance_data),
            calculate_mobile_money_score(mobile_money_data),
            calculate_purchase_score(purchase_data)
        )

        st.session_state.score_history.append({
            'timestamp': datetime.now(),
            'score': current_score
        })

        st.session_state.last_update = datetime.now()
        st.experimental_rerun()

# Display real-time monitoring charts
if st.session_state.transactions:
    st.plotly_chart(create_real_time_monitor(
        st.session_state.transactions[-20:],  # Show last 20 transactions
        st.session_state.score_history[-20:]  # Show last 20 score updates
    ), use_container_width=True)

    st.plotly_chart(create_transaction_monitoring_table(
        st.session_state.transactions[-10:]  # Show last 10 transactions
    ), use_container_width=True)

# User Profile Section
st.header("User Profile")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Name", user['name'])
with col2:
    st.metric("Age", user['age'])
with col3:
    st.metric("Employment", user['employment'])

# Calculate Scores
remittance_score = calculate_remittance_score(remittance_data)
mobile_money_score = calculate_mobile_money_score(mobile_money_data)
purchase_score = calculate_purchase_score(purchase_data)
overall_score = calculate_overall_score(remittance_score, mobile_money_score, purchase_score)
risk_category, risk_color = get_risk_category(overall_score)

# Overall Score and Risk Category
st.header("Credit Score Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(create_score_gauge(overall_score), use_container_width=True)
with col2:
    st.plotly_chart(create_risk_factors_radar(remittance_score, mobile_money_score, purchase_score),
                    use_container_width=True)

# Risk Category
st.markdown(f"### Risk Category: <span style='color:{risk_color}'>{risk_category}</span>",
           unsafe_allow_html=True)

# Detailed Analysis Sections
st.header("Detailed Analysis")

# Remittance Analysis
st.subheader("Remittance Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(create_transaction_history(remittance_data, title="Remittance History"),
                    use_container_width=True)
with col2:
    st.plotly_chart(create_category_distribution(remittance_data, 'frequency',
                                               "Remittance Frequency Distribution"),
                    use_container_width=True)

# Mobile Money Analysis
st.subheader("Mobile Money Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(create_transaction_history(mobile_money_data, title="Mobile Money Transactions"),
                    use_container_width=True)
with col2:
    st.plotly_chart(create_category_distribution(mobile_money_data, 'transaction_type',
                                               "Transaction Type Distribution"),
                    use_container_width=True)

# Purchase History Analysis
st.subheader("Purchase History Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(create_transaction_history(purchase_data, title="Purchase History"),
                    use_container_width=True)
with col2:
    st.plotly_chart(create_category_distribution(purchase_data, 'category',
                                               "Purchase Category Distribution"),
                    use_container_width=True)

# Download Report Section
st.header("Download Report")
if st.button("Generate Report"):
    report = f"""
    Credit Score Report
    ------------------
    User: {user['name']}
    Overall Score: {overall_score:.2f}
    Risk Category: {risk_category}

    Component Scores:
    - Remittance Score: {remittance_score:.2f}
    - Mobile Money Score: {mobile_money_score:.2f}
    - Purchase Score: {purchase_score:.2f}

    Recent Transactions:
    {pd.DataFrame(st.session_state.transactions[-5:]).to_string() if st.session_state.transactions else 'No recent transactions'}
    """
    st.download_button(
        label="Download Credit Report",
        data=report,
        file_name="credit_report.txt",
        mime="text/plain"
    )