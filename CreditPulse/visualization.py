import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def create_score_gauge(score, title="Credit Score"):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 60], 'color': "red"},
                {'range': [60, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
            ]
        }
    ))
    return fig

def create_transaction_history(df, value_column='amount', title="Transaction History"):
    fig = px.line(df.sort_values('date'),
                  x='date',
                  y=value_column,
                  title=title)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount",
        showlegend=True
    )
    return fig

def create_category_distribution(df, category_column, title="Category Distribution"):
    category_counts = df[category_column].value_counts()
    fig = px.pie(values=category_counts.values,
                 names=category_counts.index,
                 title=title)
    return fig

def create_risk_factors_radar(remittance_score, mobile_money_score, purchase_score):
    fig = go.Figure(data=go.Scatterpolar(
        r=[remittance_score, mobile_money_score, purchase_score],
        theta=['Remittance Score', 'Mobile Money Score', 'Purchase Score'],
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Risk Factors Analysis"
    )
    return fig

def create_real_time_monitor(transactions, score_history):
    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add transactions
    fig.add_trace(
        go.Scatter(
            x=[t['date'] for t in transactions],
            y=[t['amount'] for t in transactions],
            name="Transaction Amount",
            mode='markers+lines',
            marker=dict(size=8),
            line=dict(width=2)
        )
    )

    # Add credit score
    fig.add_trace(
        go.Scatter(
            x=[s['timestamp'] for s in score_history],
            y=[s['score'] for s in score_history],
            name="Credit Score",
            yaxis="y2",
            mode='lines',
            line=dict(width=3, dash='dot')
        )
    )

    fig.update_layout(
        title="Real-time Monitoring: Transactions and Credit Score",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Transaction Amount"),
        yaxis2=dict(
            title="Credit Score",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),
        hovermode='x unified'
    )

    return fig

def create_transaction_monitoring_table(transactions):
    df = pd.DataFrame(transactions)

    if len(df) > 0:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Time', 'Type', 'Amount', 'Status'],
                fill_color='paleturquoise',
                align='left'
            ),
            cells=dict(
                values=[
                    df['date'].dt.strftime('%Y-%m-%d %H:%M:%S'),
                    df['type'],
                    df['amount'].round(2),
                    df.apply(lambda x: x.get('payment_status', 'Completed'), axis=1)
                ],
                fill_color='lavender',
                align='left'
            )
        )])

        fig.update_layout(title="Recent Transactions")
        return fig
    return None