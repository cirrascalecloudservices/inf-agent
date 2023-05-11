#!/usr/bin/env python3

import base64
import datetime
import json
import os
import requests
import time

from urllib.parse import urlparse, parse_qs

# client -> service <- worker

# base_url='http://localhost:8080'
base_url='https://inf.san01.cirrascale.net'
# cirrascale service headers
service_headers = {'Authorization': os.environ['WORKER_APIKEY']}

while 1:
    try:
        work = {}
        work['start_at'] = datetime.datetime.now()
        work['consume_response'] = requests.post('{}/receive-request'.format(base_url), headers=service_headers)
        work['consume_response'].raise_for_status()
        if work['consume_response'].status_code == 200:
            work['context'] = work['consume_response'].json()

            # STEP 1 consume request from cirrascale service
            context = work['context']
            request_id = context['request_id']
            request_url = context['request_url']
            request_content_type = context['request_content_type']
            request_payload_base64 = context['request_payload_base64']

            # STEP 2 local request/response, e.g., local gradio web api
            local_request_headers = {'Content-Type': request_content_type}
            local_request_payload = base64.b64decode(request_payload_base64)
            work['local_response'] = requests.post('http://localhost:8000', headers=local_request_headers, data=local_request_payload)

            # TODO tunnel response errors back to client??
            # TODO tunnel response errors back to client??
            # TODO tunnel response errors back to client??
            work['local_response'].raise_for_status()
            # TODO tunnel response errors back to client??
            # TODO tunnel response errors back to client??
            # TODO tunnel response errors back to client??

            # STEP 3 produce response to cirrascale service
            context['response_content_type'] = work['local_response'].headers['Content-Type']
            context['response_payload_base64'] = base64.b64encode(work['local_response'].content).decode()
            work['produce_response'] = requests.post('{}/send-response'.format(base_url), headers=service_headers, json=context)
            work['produce_response'].raise_for_status()

    except Exception as e:
        work['e'] = e
    finally:
        work['closed_at'] = datetime.datetime.now()
        print (json.dumps(work, indent=1, default=str))
    if 'e' in work:
        # backoff
        time.sleep(2)
