# from flask import Flask, request, jsonify
# import pandas as pd
# import joblib

# # Load the trained model
# model = joblib.load('trip_time_model.pkl')

# # Load the CCVI data
# ccvidata_cleaned = pd.read_csv('ccvidata_cleaned.csv')

# app = Flask(__name__)

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()
#         pickup_area = data.get('pickup_community_area')
#         dropoff_area = data.get('dropoff_community_area')

#         if pickup_area is None or dropoff_area is None:
#             return jsonify({'error': 'Invalid input'}), 400

#         # Prepare input for the model
#         input_data = pd.DataFrame({
#             'pickup_community_area': [pickup_area],
#             'dropoff_community_area': [dropoff_area],
#             'community_area_or_zip': [dropoff_area]
#         })

#         # Predict trip time
#         trip_seconds = model.predict(input_data)[0]

#         # Get CCVI category for the dropoff area
#         ccvi_category = ccvidata_cleaned[ccvidata_cleaned['community_area_or_zip'] == dropoff_area]['ccvi_category'].values
#         ccvi_category = ccvi_category[0] if ccvi_category.size > 0 else "Unknown"

#         # Return the prediction and category
#         return jsonify({
#             'trip_seconds': trip_seconds,
#             'ccvi_category': ccvi_category
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('trip_time_model.pkl')

# Define the route for prediction
@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Get query parameters from the URL
        pickup_area = int(request.args.get('pickup_community_area'))
        dropoff_area = int(request.args.get('dropoff_community_area'))

        # Create input data for prediction
        input_data = pd.DataFrame({
            'pickup_community_area': [pickup_area],
            'dropoff_community_area': [dropoff_area],
            'community_area_or_zip': [dropoff_area]  # Assuming this matches for prediction
        })

        # Predict trip time using the linear regression model
        predicted_time = model.predict(input_data)[0]

        # Create a response dictionary
        response = {
            'pickup_community_area': pickup_area,
            'dropoff_community_area': dropoff_area,
            'predicted_trip_time_seconds': predicted_time
        }

        # Return the prediction as a JSON response
        return jsonify(response)

    except Exception as e:
        # Return an error message in case of an exception
        return jsonify({'error': str(e)}), 400

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
