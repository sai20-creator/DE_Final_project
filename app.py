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

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("pickup_area", "INT64", pickup_area),
            bigquery.ScalarQueryParameter("dropoff_area", "INT64", dropoff_area)
        ]
    )

    # Run the query
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    for row in results:
        trip_time = row['predicted_trip_seconds']
    
    return render_template('result.html', trip_time=trip_time)

if __name__ == '__main__':
    app.run(debug=True)

