import boto3
import re
import json
from datetime import datetime
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

class ESLambdaLog:
	def __init__(self, index_name = ""):
		index_day_text = datetime.now().strftime("%Y.%m.%d")
		self.index_name = "aws_lambda_log_" + index_name + "." + index_day_text

		es_host = 'search-ziegler-es-bnlsbjliclp6ebc67fu3mfr74u.us-east-1.es.amazonaws.com'
		auth = BotoAWSRequestsAuth(aws_host=es_host,
											aws_region='us-east-1',
											aws_service='es')

		# use the requests connection_class and pass in our custom auth class
		self.es = Elasticsearch(host=es_host, use_ssl=True, port=443, connection_class=RequestsHttpConnection, http_auth=auth)	
		

		indices = self.list_indices()
		if self.index_name not in indices:
			mappings = {
					"mappings": {
						"doc": {
							"properties": {
								"@timestamp": {
									"type": "date"
							}
						}
					}
				}
			}
			self.es.indices.create(self.index_name, body=mappings)


	def get_timestamp(self):
		return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

	def log_event(self, event):
		if "@timestamp" not in event:
			event["@timestamp"] = self.get_timestamp()
		self.es.index(index=self.index_name, doc_type = "doc", body = event)
		print("Added to " + self.index_name)


	def list_indices(self):
		results = self.es.indices.get(index = "*")
		list = []
		for index_name in results.keys():
			list.append(index_name)
		return list