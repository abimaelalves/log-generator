import json
import time
import random
import string
import os

LOG_FILE = "/fluentbit/logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Payload 1: com x-device-id
PAYLOAD_WITH_DEVICE_ID = {
    "message": "Request and Response Digest",
    "level": "INFO",
    "level_value": 20000,
    "dd.service": "im2-caronte",
    "dd.env": "hom",
    "dd.version": "V1",
    "communication": {
        "request": {
            "headers": {
                "x-itau-correlationid": ["f3e2689d-deda-4f63-b645-ef4fec6b9da7"],
                "x-init-id": ["d3c44e96-cdb7-4a07-81d7-61182bf98b9b"]
            },
            "method": "POST",
            "id": "a89508de-2952767",
            "URI": "https://trackabilities-collector.api-sp.hom.aws.cloud.ihf/v1/collect"
        },
        "response": {
            "status_code": "200",
            "request_time_taken": 45
        }
    },
    "logSecurity": {
        "charonId": "4tb2blnt",
        "sessionId": "1c7a8b20-d02b-4b30-a4ba-a66bee4a3b8f",
        "flowId": "a89508de-2952767",
        "remoteIp": "172.20.57.34",
        "userAgent": "android",
        "hostname": "612afdc91ffe"
    }
}

# Payload 2: sem x-device-id
PAYLOAD_NO_DEVICE_ID = {
    "message": "Request and Response Digest",
    "level": "INFO",
    "level_value": 20000,
    "dd.service": "im2-caronte",
    "dd.env": "hom",
    "dd.version": "V1",
    "communication": {
        "request": {
            "headers": {
                "x-itau-correlationid": ["eddc2570-2952766"],
                "x-init-id": ["abcd1234-init-5678"]
            },
            "method": "GET",
            "id": "eddc2570-2952766",
            "URI": "https://campanhas-v1-ofertas-produtos.api-sp.hom.aws.cloud.ihf/campanhas/v1"
        },
        "response": {
            "status_code": "403",
            "request_time_taken": 142
        }
    },
    "logSecurity": {
        "charonId": "2a1eayv3",
        "sessionId": "a5bd1da2-2bbb-475b-91cc-a24ff662cf64",
        "flowId": "eddc2570-2952766",
        "remoteIp": "79.127.208.242",
        "userAgent": "Windows",
        "hostname": "612afdc91ffe"
    }
}

def generate_trace_id():
    return str(random.getrandbits(64))

def generate_span_id():
    return str(random.getrandbits(64))

def generate_device_id(length=64):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def emit_logs():
    toggle = True
    while True:
        base = PAYLOAD_WITH_DEVICE_ID if toggle else PAYLOAD_NO_DEVICE_ID
        payload = json.loads(json.dumps(base))  # deep copy
        payload["@timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        payload["@version"] = "1"
        payload["thread_name"] = "reactor-http-epoll-" + str(random.randint(1, 5))
        payload["dd.trace_id"] = generate_trace_id()
        payload["dd.span_id"] = generate_span_id()

        if toggle:
            payload["communication"]["request"]["headers"]["x-device-id"] = [generate_device_id()]

        log_line = json.dumps(payload)
        print(log_line, flush=True)
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")

        time.sleep(3)
        toggle = not toggle

if __name__ == "__main__":
    emit_logs()
