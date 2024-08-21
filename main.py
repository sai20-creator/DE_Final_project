import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

ccvidata_cleaned = pd.read_csv('ccvidata_cleaned.csv')
transportdata_cleaned = pd.read_csv('transportdata_cleaned.csv')

ccvi_high = ccvidata_cleaned[ccvidata_cleaned['ccvi_category'] == 'HIGH']

merged_data = pd.merge(transportdata_cleaned, ccvi_high,
                       left_on='pickup_community_area', right_on='community_area_or_zip')

features = ['pickup_community_area', 'dropoff_community_area', 'community_area_or_zip']
target = 'trip_seconds'

X = merged_data[features]
y = merged_data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction on Local
y_pred = model.predict(X_test)

# model performance
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)

joblib.dump(model, 'trip_time_model.pkl')
