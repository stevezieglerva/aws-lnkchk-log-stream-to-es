import gzip
import json
import base64
import re
from ESLambdaLog import *
from Event import *
import logging
import structlog
import sys
import datetime


def lambda_handler(event, context):
    log = setup_logging()
    log = log.bind(lambda_name="aws-lnkchk-stream-to-es")
    if context is not None:
        log = log.bind(aws_request_id=context.aws_request_id)
    log.critical("started", input_events=json.dumps(event, indent=3))
    log.critical("starting_log-stream-to-es")

    cw_data = event["awslogs"]["data"]
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    log_events = payload["logEvents"]
    print("Total log events received: " + str(len(log_events)))
    count = 0
    count = process_cloud_watch_messages(log_events) 
    print("Processed JSON log events:" + str(count))
    log.critical("finished_log-stream-to-es", processed_count=count)
    return {"processed_structlog_messages" : count}


def process_cloud_watch_messages(log_events):
    log = structlog.get_logger()
    log.critical("event_json_log_count", record_json_log_count=len(log_events), log_events=log_events)
    print("*** log_events:")
    json_log_count = 0
    for log_event in log_events:
        message = log_event["message"]
        if "{" in message and "lambda_name" in message:
            print(str(json_log_count) + " - " + message)
            #timestamp = extract_timestamp_from_message_line(message)
            json_string = re.sub("^[^{]+", "", message)
            try:
                print("*** here is the original json_string: " + json_string)
                json_object = json.loads(json_string)
            #    json_object["@timestamp"] = timestamp

                index_name = ""
                if "lambda_name" in json_object:
                    index_name = json_object["lambda_name"]

                print("Adding to event stream also")
                create_es_event(json_object)
                json_log_count = json_log_count + 1
            except Exception as e:
                print("Exception")
                print(e)
                print("Continuing to next message")
    return json_log_count


def extract_timestamp_from_message_line(message):
    chars_until_first_close_bracket_and_space = "^[^]]+\]( |\t)"
    timestamp = re.sub(chars_until_first_close_bracket_and_space, "", message) 
    chars_from_space_on = "( |\t).*$"
    timestamp = re.sub(chars_from_space_on, "", timestamp) 
    final_chars = "Z.*$"
    timestamp = re.sub(final_chars, "", timestamp) 
    timestamp = re.sub("\n", "", timestamp) 
    if "2018" not in timestamp:
        raise Exception("Extracting timestamp did not return a date")
    return timestamp


def extract_json_from_message_line(message):
    print("||| Input: " + message)
    json_string = re.sub("^[^{]+", "", message)
    print("||| Output: " + json_string)
    return json_string


def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()
