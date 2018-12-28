import boto3
from LocalTime import *
import json
from S3TextFromLambdaEvent import *

class Event:

	def __init__(self, dynamoDB_table, event_text):
		db = boto3.client("dynamodb")
		local_time = LocalTime()
		try:
			response = db.put_item(TableName = dynamoDB_table, 
				Item = {"key_indicator" : {"S" : "event_" + str(local_time.get_utc_epoch())}, 
				"event" : {"S" : json.dumps(event_text)},
				"ttl" : {"N" : str(local_time.get_utc_epoch())}, 
				"timestamp" : {"S" : str(local_time.utc)}, 
				"timestamp_local" : {"S" : str(local_time.local)}}) 

			s3 = boto3.resource("s3")
			create_s3_text_file("code-index", "es-bulk-files-input/" + str(local_time.get_utc_epoch()) + ".json", json.dumps(event_text), s3)
			
		except Exception as e:
			print("Exception")
			print(e)
			raise(e)

		
	def purge_event(self, dynamoDB_table, event_text):
		db = boto3.client("dynamodb")
		response = db.delete_item(TableName = dynamoDB_table, 
			Item = {"s3-url" : {"S" : event_text}})
		
		