import boto3
from LocalTime import *
import json
from S3TextFromLambdaEvent import *
import uuid


def create_es_event(data, index = "", id = "", ):
	local_time = LocalTime()
	s3 = boto3.resource("s3")

	if index == "":
		#aws_lambda_log_aws-s3-queue-prep.2018.12.28
		lambda_name = ""
		if "lambda_name" in data:
			lambda_name = data["lambda_name"]
		index = "aws_lambda_log_" + lambda_name

	filename_id = ""
	if id == "":
		id = str(uuid.uuid4())
		filename_id = id
	else:
		filename_id = str(uuid.uuid4())	

	if "@timestamp" not in data:
		data["@timestamp"] = local_time.get_utc_timestamp()

	if "@timestamp_local" not in data:
		data["@timestamp_local"] = local_time.get_local_timestamp()

	es_queue_event = {"_index" : index, "_id" : id, "data" : data}
	message_text_string =  json.dumps(es_queue_event)
	print("*** message_text_string: " + message_text_string)
	filename = "es-bulk-files-input/" + index + "_" + filename_id + ".json"

	response = create_s3_text_file("code-index", filename, message_text_string, s3)
	s3_url = "https://s3.amazonaws.com/code-index/" + filename
	return s3_url

