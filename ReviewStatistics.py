import argparse
import itertools
import logging
import os
import requests
import time
from datetime import datetime
import json, csv, sys


logging.basicConfig(format = '|%(asctime)s| %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def request_for_completed(token, start_date, end_date):
	headers = {'Authorization': token, 'Content-Length': '0'}
	start_date = start_date
	end_date = end_date

	request_url = 'https://review-api.udacity.com/api/v1/me/submissions/completed.json'
	payload = {}

	if start_date is not None and end_date is not None:
		payload = {'start_date' : start_date, 'end_date' : end_date}
		logger.info("Request to {}".format(str(request_url)))

	logger.info("Requesting completed projects...")
	completed_resp = requests.get(request_url, headers=headers, params = payload)
	completed_resp.raise_for_status()
	completed = completed_resp.json()
	return completed

def output_to_csv(token, start_date, end_date):
	completed_project_list = request_for_completed(token, start_date, end_date)
	filename = "review_completed" + start_date + end_date + '.csv'
	with open(filename, 'wb') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter = ',')
		header = ['ID', 'Project ID', 'User', 'Project Name','Result', 'Completed On', 'Price']
		csv_writer.writerow (header)
		for project in completed_project_list:
			row = [project['id'], project['project_id'], project['user']['name'],
			project['project']['name'], project['result'], datetime.strptime(project['completed_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date(),
			project['price']]

			csv_writer.writerow(row)



if __name__=="__main__":
    token = str(sys.argv[1])
    start_date = str(sys.argv[2])
    end_date = str(sys.argv[3])

    output_to_csv(token, start_date, end_date)