import joblib
import pandas as pd

model = joblib.load('trip_time_model.pkl')

pickup_area = 1
dropoff_area = 2

input_data = pd.DataFrame({
    'pickup_community_area': [pickup_area],
    'dropoff_community_area': [dropoff_area],
    'community_area_or_zip': [dropoff_area]
})
predicted_time = model.predict(input_data)[0]
print("Predicted trip time (seconds):", predicted_time)
