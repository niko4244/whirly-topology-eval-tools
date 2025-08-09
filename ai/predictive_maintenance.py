"""
Predictive Maintenance: Forecast failures from historical sensor data.
"""
import pandas as pd
from sklearn.linear_model import LinearRegression

class MaintenancePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, history_df):
        X = history_df[['usage_hours', 'avg_temp', 'load_cycles']]
        y = history_df['time_to_failure']
        self.model.fit(X, y)

    def predict_failure(self, usage, temp, cycles):
        return self.model.predict([[usage, temp, cycles]])[0]