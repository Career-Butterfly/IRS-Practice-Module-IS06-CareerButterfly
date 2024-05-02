from io import StringIO
from flask import Flask, request
import pandas as pd

app = Flask(__name__)

COMPANY_SCORES_CSV = '/data/company_scores.csv'
COMPANY_SCORES_AGGREGATE_CSV = '/data/company_scores_aggregate.csv'

@app.route("/ping")
def ping():
    return "Pinged"

def handle_get_company_reviews(request, company_reviews):
    if 'company_name' in request.args.keys():
        company_name_list_lower = [name.lower() for name in request.args['company_name'].split(',')]
        company_reviews = company_reviews[company_reviews['company_name'].str.lower().isin(company_name_list_lower)]
    if 'job_title' in request.args.keys():
        job_title_list_lower = [job_title.lower() for job_title in request.args['job_title'].split(',')]
        company_reviews = company_reviews[company_reviews['job_position_category'].str.lower().isin(job_title_list_lower)]
    accept = request.headers.get('Accept', '')
    # Returns json
    if 'application/json' in accept:
        return company_reviews.to_json(orient='records')
    # Returns csv by default
    else:
        s = StringIO()
        company_reviews.to_csv(s)
        return s.getvalue()

@app.route("/", methods=['GET'])
def get_sentiment():
    company_reviews = pd.read_csv(COMPANY_SCORES_CSV)
    return handle_get_company_reviews(request, company_reviews)

@app.route("/aggregate", methods=['GET'])
def get_aggregated_sentiment():
    company_reviews = pd.read_csv(COMPANY_SCORES_AGGREGATE_CSV)
    return handle_get_company_reviews(request, company_reviews)
    
@app.route("/job_title", methods=['GET'])
def get_job_title():
    company_reviews = pd.read_csv(COMPANY_SCORES_CSV)
    job_title_list = company_reviews['job_position_category'].unique()
    return job_title_list.tolist()

@app.route("/company", methods=['GET'])
def get_company():
    company_reviews = pd.read_csv(COMPANY_SCORES_CSV)
    company_list = company_reviews['company_name'].unique()
    return company_list.tolist()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8100, debug=True)