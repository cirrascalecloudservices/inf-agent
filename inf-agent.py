#!/usr/bin/env python3

import base64
import datetime
import json
import os
import requests
import time
import urllib.parse

from_url = os.environ['FROM'] # e.g., 'https://bert.inf.san01.cirrascale.net'
to_url = os.environ['TO'] # e.g., http://localhost:7860
cirrascale_headers = {'Authorization': os.environ['WORKER_APIKEY']}

while 1:
    try:
        work = {}
        work['start_at'] = datetime.datetime.now()
        consume_response = work['consume_response'] = requests.post('{}/receive-request'.format(from_url), headers=cirrascale_headers)
        consume_response.raise_for_status()
        if consume_response.status_code == 200:
            context = work['context'] = consume_response.json()

            # STEP 1 consume request from cirrascale service
            request_id = context['request_id']
            request_url = urllib.parse.urlparse(context['request_url'])
            request_content_type = context['request_content_type']
            request_payload_base64 = context['request_payload_base64']

            # STEP 2 local request/response, e.g., local gradio web api
            local_request_headers = {'Content-Type': request_content_type}
            local_request_payload = base64.b64decode(request_payload_base64)
            # TODO use urllib to build url here
            # TODO use urllib to build url here
            # TODO use urllib to build url here
            local_url = '{}{}'.format(to_url, request_url.path) # e.g., http://localhost:7860/api/predict
            # TODO use urllib to build url here
            # TODO use urllib to build url here
            # TODO use urllib to build url here
            local_response = work['local_response'] = requests.post(local_url, headers=local_request_headers, data=local_request_payload)

            # STEP 3 produce response to cirrascale service
            context['response_code'] = local_response.status_code
            context['response_content_type'] = local_response.headers['Content-Type']
            context['response_payload_base64'] = base64.b64encode(local_response.content).decode()
            produce_response = work['produce_response'] = requests.post('{}/send-response'.format(from_url), headers=cirrascale_headers, json=context)
            produce_response.raise_for_status()

    except Exception as e:
        work['e'] = e
        time.sleep(2)
    
    finally:
        work['closed_at'] = datetime.datetime.now()
        print (json.dumps(work, indent=1, default=str), flush=True)
