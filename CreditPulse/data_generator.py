import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_remittance_data(n_records=1000):
    data = {
        'transaction_id': [fake.uuid4() for _ in range(n_records)],
        'date': [(datetime.now() - timedelta(days=np.random.randint(1, 365))) for _ in range(n_records)],
        'amount': np.random.normal(500, 200, n_records),
        'sender_country': [fake.country() for _ in range(n_records)],
        'frequency': np.random.choice(['Weekly', 'Monthly', 'Quarterly'], n_records)
    }
    df = pd.DataFrame(data)
    df = df.sort_values('date')
    return df

def generate_mobile_money_data(n_records=1000):
    data = {
        'transaction_id': [fake.uuid4() for _ in range(n_records)],
        'date': [(datetime.now() - timedelta(days=np.random.randint(1, 365))) for _ in range(n_records)],
        'amount': np.random.normal(100, 50, n_records),
        'transaction_type': np.random.choice(['Send', 'Receive', 'Bill Payment'], n_records),
        'balance_after': np.random.normal(1000, 300, n_records)
    }
    df = pd.DataFrame(data)
    df = df.sort_values('date')
    return df

def generate_purchase_history(n_records=1000):
    data = {
        'purchase_id': [fake.uuid4() for _ in range(n_records)],
        'date': [(datetime.now() - timedelta(days=np.random.randint(1, 365))) for _ in range(n_records)],
        'amount': np.random.normal(200, 100, n_records),
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Services'], n_records),
        'payment_status': np.random.choice(['Completed', 'Pending', 'Failed'], n_records, p=[0.8, 0.15, 0.05])
    }
    df = pd.DataFrame(data)
    df = df.sort_values('date')
    return df

def generate_user_profile():
    return {
        'user_id': fake.uuid4(),
        'name': fake.name(),
        'age': np.random.randint(21, 65),
        'employment': np.random.choice(['Employed', 'Self-employed', 'Business Owner']),
        'monthly_income': np.random.normal(5000, 1500)
    }

def generate_real_time_transaction():
    """Generate a single real-time transaction for monitoring"""
    transaction_type = np.random.choice(['Remittance', 'Mobile Money', 'Purchase'])

    if transaction_type == 'Remittance':
        return {
            'type': transaction_type,
            'transaction_id': fake.uuid4(),
            'date': datetime.now(),
            'amount': np.random.normal(500, 200),
            'sender_country': fake.country(),
            'frequency': np.random.choice(['Weekly', 'Monthly', 'Quarterly'])
        }
    elif transaction_type == 'Mobile Money':
        return {
            'type': transaction_type,
            'transaction_id': fake.uuid4(),
            'date': datetime.now(),
            'amount': np.random.normal(100, 50),
            'transaction_type': np.random.choice(['Send', 'Receive', 'Bill Payment']),
            'balance_after': np.random.normal(1000, 300)
        }
    else:  # Purchase
        return {
            'type': transaction_type,
            'purchase_id': fake.uuid4(),
            'date': datetime.now(),
            'amount': np.random.normal(200, 100),
            'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Services']),
            'payment_status': np.random.choice(['Completed', 'Pending', 'Failed'], p=[0.8, 0.15, 0.05])
        }