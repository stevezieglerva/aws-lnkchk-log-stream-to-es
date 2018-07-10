import gzip
import json
import base64
import re
from ESLambdaLog import *


def lambda_handler(event, context):
    es = ESLambdaLog("aws_test_log_sync")

    cw_data = event["awslogs"]["data"]
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    log_events = payload["logEvents"]
    for log_event in log_events:
        print("_______________________")
        json_event_only = ""
        message = log_event["message"]
        print("message: ")
        print(message)
        if "{" in message:
            json_string = re.sub("^[^{]+", "", message)
            print("json_string:")
            print(json_string)
            json_object = json.loads(json_string)
            print(json.dumps(json_object, indent=True))

            # Send the log event into Elasticsearch
            es.log_event(json_object)


