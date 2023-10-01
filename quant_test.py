#! /usr/bin/env python
# run tests in quant_test.json on koboldcpp endpoint
# run python3 koboldcpp.py --model <name> --usecublas --debugmode --gpulayers x

import sys
import json
import pprint
import requests

def send_generate_request(options, headers = None):
    url = "http://127.0.0.1:5001/api/v1/generate"
    url2 = "http://127.0.0.1:5000/api/v1/generate"

    if headers == None:
        headers = { "accept": "application/json", "Content-Type": "application/json" }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(options))
        if response.status_code == 200:
            return response
        else:
            response = requests.post(url2, headers=headers, data=json.dumps(options))
            if response.status_code == 200:
                return response
            else:
                print("Failed 2x with status_code: " + str(response.status_code))
    except ConnectionError as e:
        print(f"Error connecting to local API: {e}")

    return {}

def test_start(options, tests):
    log = pprint.PrettyPrinter()
    #log.pprint(options)
    #log.pprint(tests)

    responses = []
    count = 0
    total_tests = len(tests)

    for test in tests:
        count += 1
        print(f"{test['label']} - Test {count}/{total_tests}")
        print(test["test"] + "\n")

        options["prompt"] = test["test"]
        response = send_generate_request(options)
        data = response.json()

        answer = data["results"][0]["text"]
        print(answer + "\n")

        test["result"] = answer
        responses.append(test)

    with open("responses.json", "w") as f:
        f.write(json.dumps(responses, indent=4))


def main():
    options = {
        "n": 1,
        "max_context_length": 4096,
        "max_length": 800,
        "rep_pen": 1.1,
        "temperature": 0,
        "top_p": 0,
        "top_k": 1,
        "top_a": 0,
        "typical": 1,
        "tfs": 1,
        "rep_pen_range": 4096,
        "rep_pen_slope": 0.2,
        "sampler_order": [6, 0, 1, 3, 4, 2, 5],
        "quiet": True,
        "stop_sequence": ["You:", "\nYou ", "\n\n\n"],
        "prompt": "",
    }

    if len(sys.argv) != 1:
        print("Usage: python3 quant_test.py")
        print(sys.argv)
        sys.exit(1)

    with open("quant_test.json") as jsonfile:
        tests = json.loads(jsonfile.read())

    test_start(options, tests)

if __name__ == "__main__":
    main()

###
