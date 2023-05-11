#!/usr/bin/env python3

import base64
import datetime
import json
import os
import requests
import time
import urllib.parse

# client -> service <- worker

# e.g., http://localhost:7860
local_url = os.environ['URL']

# cirrascale_url='http://localhost:8080'
cirrascale_url='https://inf.san01.cirrascale.net'
cirrascale_service_headers = {'Authorization': os.environ['WORKER_APIKEY']}

while 1:
    try:
        work = {}
        work['start_at'] = datetime.datetime.now()
        work['consume_response'] = requests.post('{}/receive-request'.format(cirrascale_url), headers=cirrascale_service_headers)
        work['consume_response'].raise_for_status()
        if work['consume_response'].status_code == 200:
            work['context'] = work['consume_response'].json()

            # STEP 1 consume request from cirrascale service
            context = work['context']
            request_id = context['request_id']
            request_url = urllib.parse.urlparse(context['request_url'])
            request_content_type = context['request_content_type']
            request_payload_base64 = context['request_payload_base64']

            # STEP 2 local request/response, e.g., local gradio web api
            local_request_headers = {'Content-Type': request_content_type}
            local_request_payload = base64.b64decode(request_payload_base64)

            # TODO use urlib to build url here
            # TODO use urlib to build url here
            # TODO use urlib to build url here
            url = '{}{}'.format(local_url, request_url.path) # e.g., http://localhost:7860/api/predict
            # TODO use urlib to build url here
            # TODO use urlib to build url here
            # TODO use urlib to build url here
            work['local_response'] = requests.post(url, headers=local_request_headers, data=local_request_payload)

            # TODO tunnel local response errors back to client??
            # TODO tunnel local response errors back to client??
            # TODO tunnel local response errors back to client??
            work['local_response'].raise_for_status()
            # TODO tunnel local response errors back to client??
            # TODO tunnel local response errors back to client??
            # TODO tunnel local response errors back to client??

            # STEP 3 produce response to cirrascale service
            context['response_content_type'] = work['local_response'].headers['Content-Type']
            context['response_payload_base64'] = base64.b64encode(work['local_response'].content).decode()
            work['produce_response'] = requests.post('{}/send-response'.format(cirrascale_url), headers=cirrascale_service_headers, json=context)
            work['produce_response'].raise_for_status()

    except Exception as e:
        work['e'] = e
        time.sleep(2)
    finally:
        work['closed_at'] = datetime.datetime.now()
        print (json.dumps(work, indent=1, default=str))
