# -*- coding: utf-8 -*-
"""flight_prediction.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GhKRg5FMi37SA5j1gabNuzWxhStDxq2O
"""

import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import Lasso
df = pd.read_csv(r'c:\Users\hp5cd\OneDrive\Desktop\React\Flight-Predictor\src\data\flight_dataset.csv')
df['Combined_Date'] = df.apply(lambda row: f"{row['Date']:02d}-{row['Month']:02d}-{row['Year']}", axis=1)
df['Day'] = pd.to_datetime(df['Combined_Date'], format='%d-%m-%Y').dt.day_name()
grouped_by_airline = df.groupby('Airline')
label_encoder = preprocessing.LabelEncoder()
label_encoder.fit(df["Source"])
df["Source"] = label_encoder.transform(df["Source"])
label_encoder.fit(df['Destination'])
df['Destination'] = label_encoder.transform(df['Destination'])
label_encoder.fit(df['Day'])
df['Day'] = label_encoder.transform(df['Day'])
def train_and_save_model(df):
    features = ['Source','Destination','Total_Stops','Day','Month']
    target = ['Price','Duration_hours','Duration_min']
    X = df[features]
    y = df[target]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = Lasso(alpha=1.0)
    model.fit(X_scaled, y)
    with open('trained_model.pkl', 'wb') as file:
        pickle.dump(model, file)
    with open('scaler.pkl', 'wb') as file:
        pickle.dump(scaler, file)
    return model, scaler
model, scaler = train_and_save_model(df)
with open('trained_model.pkl', 'rb') as file:
    model = pickle.load(file)
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)
def apply_lasso_linear_regression(df, airline_name, model, scaler):
    features = ['Source','Destination','Total_Stops','Day','Month']
    target = ['Price','Duration_hours','Duration_min']
    X = df[features]
    y = df[target]
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)
    print("Airline : ", airline)
    print("Predicted Price : ", y_pred[0][0])
    print("Predicted Duration (hours) : ", y_pred[0][1])
    print("Predicted Duration (minutes) : ", y_pred[0][2])
for airline, group in grouped_by_airline:
    apply_lasso_linear_regression(group, airline, model, scaler)