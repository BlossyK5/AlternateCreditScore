import pandas as pd
import numpy as np

def calculate_remittance_score(remittance_data):
    # Calculate average monthly remittance
    monthly_avg = remittance_data.groupby(remittance_data['date'].dt.to_period('M'))['amount'].mean()
    
    # Calculate frequency score
    frequency_counts = remittance_data['frequency'].value_counts()
    frequency_score = (frequency_counts['Weekly'] * 1.0 + frequency_counts['Monthly'] * 0.7 + 
                      frequency_counts['Quarterly'] * 0.4) / len(remittance_data)
    
    return (monthly_avg.mean() / 1000 * 30 + frequency_score * 70)

def calculate_mobile_money_score(mobile_money_data):
    # Calculate average balance
    avg_balance = mobile_money_data['balance_after'].mean()
    
    # Calculate transaction frequency
    transaction_frequency = len(mobile_money_data) / (mobile_money_data['date'].max() - 
                                                    mobile_money_data['date'].min()).days
    
    # Calculate success rate
    success_rate = 1 - (mobile_money_data['transaction_type'].value_counts().get('Failed', 0) / 
                       len(mobile_money_data))
    
    return (min(avg_balance / 2000, 1) * 40 + min(transaction_frequency * 10, 1) * 30 + 
            success_rate * 30)

def calculate_purchase_score(purchase_history):
    # Calculate payment reliability
    payment_reliability = (purchase_history['payment_status'] == 'Completed').mean()
    
    # Calculate purchase frequency
    purchase_frequency = len(purchase_history) / (purchase_history['date'].max() - 
                                                purchase_history['date'].min()).days
    
    # Calculate average purchase amount
    avg_purchase = purchase_history['amount'].mean()
    
    return (payment_reliability * 40 + min(purchase_frequency * 15, 1) * 30 + 
            min(avg_purchase / 500, 1) * 30)

def calculate_overall_score(remittance_score, mobile_money_score, purchase_score):
    weights = {
        'remittance': 0.35,
        'mobile_money': 0.35,
        'purchase': 0.30
    }
    
    overall_score = (remittance_score * weights['remittance'] + 
                    mobile_money_score * weights['mobile_money'] + 
                    purchase_score * weights['purchase'])
    
    return min(max(overall_score, 0), 100)

def get_risk_category(score):
    if score >= 80:
        return 'Low Risk', 'green'
    elif score >= 60:
        return 'Moderate Risk', 'yellow'
    else:
        return 'High Risk', 'red'
