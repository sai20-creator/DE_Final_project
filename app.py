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

# -----------------------------------------------------------------------------------------------------------------

# from flask import Flask, request, jsonify
# import joblib
# import pandas as pd

# app = Flask(__name__)

# # Load the pre-trained model
# model = joblib.load('trip_time_model.pkl')

# # Define the route for prediction
# @app.route('/predict', methods=['GET'])
# def predict():
#     try:
#         # Get query parameters from the URL
#         pickup_area = int(request.args.get('pickup_community_area'))
#         dropoff_area = int(request.args.get('dropoff_community_area'))

#         # Create input data for prediction
#         input_data = pd.DataFrame({
#             'pickup_community_area': [pickup_area],
#             'dropoff_community_area': [dropoff_area],
#             'community_area_or_zip': [dropoff_area]  # Assuming this matches for prediction
#         })

#         # Predict trip time using the linear regression model
#         predicted_time = model.predict(input_data)[0]

#         # Create a response dictionary
#         response = {
#             'pickup_community_area': pickup_area,
#             'dropoff_community_area': dropoff_area,
#             'predicted_trip_time_seconds': predicted_time
#         }

#         # Return the prediction as a JSON response
#         return jsonify(response)

#     except Exception as e:
#         # Return an error message in case of an exception
#         return jsonify({'error': str(e)}), 400

# # Run the app
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

# -----------------------------------------------------------------------------------------------------------------

# from flask import Flask, render_template, request
# import pandas as pd
# import joblib   

# app = Flask(__name__)

# # Load the trained model (replace with your model's path)
# model_path = 'trip_time_model.pkl'
# model = joblib.load('trip_time_model.pkl')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Get user inputs
#         pickup_area = int(request.form['pickup_area'])
#         dropoff_area = int(request.form['dropoff_area'])

#         # Prepare input data for the model
#         input_data = pd.DataFrame({
#             'pickup_community_area': [pickup_area],
#             'dropoff_community_area': [dropoff_area],
#             'community_area_or_zip': [dropoff_area]  # Assuming dropoff area is the relevant zip
#         })

#         # Make the prediction
#         predicted_time = model.predict(input_data)[0]

#         # Render the results on the page
#         return render_template('index.html', predicted_time=predicted_time, pickup_area=pickup_area, dropoff_area=dropoff_area)

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
# -----------------------------------------------------------------------------------------------------------------


# from flask import Flask, render_template, request
# from google.cloud import bigquery

# app = Flask(__name__)

# # Initialize BigQuery client
# client = bigquery.Client()

# # Set your GCP project ID and dataset ID
# project_id = 'de-week-7'
# dataset_id = 'mergeddata'
# model_id = 'trip_time_model'

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Get input from form
#         pickup_area = int(request.form['pickup_area'])
#         dropoff_area = int(request.form['dropoff_area'])

#         # BigQuery SQL query to get prediction
#         query = f"""
#         SELECT
#           predicted_trip_seconds,
#           pickup_community_area,
#           dropoff_community_area,
#           predicted_trip_seconds
#         FROM
#           ML.PREDICT(MODEL `{project_id}.{dataset_id}.{model_id}`,
#             (SELECT
#               {pickup_area} AS pickup_community_area,
#               {dropoff_area} AS dropoff_community_area,
#               community_area_or_zip,
#               FROM
#                `{project_id}.{dataset_id}.{model_id}`

#             ))
#         """

#         # Execute the query
#         query_job = client.query(query)
#         results = query_job.result()

#         # Fetch the prediction result
#         for row in results:
#             predicted_time = row['predicted_trip_seconds']

#         return render_template('index.html', predicted_time=predicted_time)

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
# -----------------------------------------------------------------------------------------------------------------

# from google.cloud import bigquery

# client = bigquery.Client()
# project_id = 'de-week-7'
# dataset_id = 'mergeddata'
# model_id = 'trip_time_model'

# query = """
# SELECT
#   predicted_trip_seconds
# FROM
#     ML.PREDICT(MODEL `{project_id}.{dataset_id}.{model_id}`,
#     (
#       SELECT
#         CAST(@pickup_area AS INT64) AS pickup_community_area,
#         CAST(@dropoff_area AS INT64) AS dropoff_community_area,
#         CAST(@dropoff_area AS INT64) AS community_area_or_zip
#         FROM
#         `{project_id}.{dataset_id}.{model_id}`
#     )
#   )
# """

# job_config = bigquery.QueryJobConfig(
#     query_parameters=[
#         bigquery.ScalarQueryParameter("pickup_area", "FLOAT64", pickup_area),
#         bigquery.ScalarQueryParameter("dropoff_area", "FLOAT64", dropoff_area)
#     ]
# )

# query_job = client.query(query, job_config=job_config)
# results = query_job.result()

# for row in results:
#     print(f"Predicted trip time (seconds): {row['predicted_trip_seconds']}")
# -----------------------------------------------------------------------------------------------------------------


from flask import Flask, request, render_template
from google.cloud import bigquery

app = Flask(__name__)

# Initialize BigQuery client
client = bigquery.Client()
project_id = 'de-week-7'
dataset_id = 'mergeddata'
model_id = 'trip_time_model'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve user input
    pickup_area = request.form.get('pickup_area')
    dropoff_area = request.form.get('dropoff_area')

    # Ensure inputs are integers
    try:
        pickup_area = int(pickup_area)
        dropoff_area = int(dropoff_area)
    except ValueError:
        return "Invalid input. Please enter valid integers."

    # Prepare the query
    query = """
    SELECT
      predicted_trip_seconds
    FROM
        ML.PREDICT(MODEL `de-week-7.mergeddata.trip_time_model`,
        (
          SELECT
            CAST(@pickup_area AS INT64) AS pickup_community_area,
            CAST(@dropoff_area AS INT64) AS dropoff_community_area,
            CAST(@dropoff_area AS INT64) AS community_area_or_zip
            FROM
            `de-week-7.mergeddata.FinalData`
        )
      )
    """

    # Set up query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("pickup_area", "INT64", pickup_area),
            bigquery.ScalarQueryParameter("dropoff_area", "INT64", dropoff_area)
        ]
    )

    # Run the query
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Process the results
    for row in results:
        trip_time = row['predicted_trip_seconds']
    
    return render_template('result.html', trip_time=trip_time)

if __name__ == '__main__':
    app.run(debug=True)

