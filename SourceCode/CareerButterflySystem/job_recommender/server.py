# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:57:43 2024

@author: kuany
"""

from flask import Flask, request
from job_recommender import job_recommender
import urllib.parse

app = Flask(__name__)

def read_resume_and_candidate_info(request):
    """
    Returns a dictionary with candidate preferences and resume information
    
    Input:
        Get Request string
    Output:
        dictionary containing candidate preferences and resume information
    """
    candidate_preference_dict = request.args.get('candidate_preferences')
    resume_info_dict = request.args.get('resume_info')
    #candidate_preference_dict = candidate_preference_dict.replace('%7B', '{').replace('%7D', '}').replace('%22', '"').replace('%5B', '[').replace('%5D', ']').replace( '%2F', '/').replace('%27', "'")
    #resume_info_dict = resume_info_dict.replace('%7B', '{').replace('%7D', '}').replace('%22', '"').replace('%5B', '[').replace('%5D', ']').replace( '%2F', '/').replace('%27', "'")
    candidate_preference_dict = urllib.parse.unquote(candidate_preference_dict)
    resume_info_dict = urllib.parse.unquote(resume_info_dict)
    resume_data = {}
    resume_data['candidate_preferences'] = candidate_preference_dict
    resume_data['resume_info'] = resume_info_dict

    return resume_data

@app.route("/ping")
def ping():
    return 'ping'

@app.route("/", methods=['GET'])
def output():
    resume_data = read_resume_and_candidate_info(request)
    return job_recommender(resume_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)