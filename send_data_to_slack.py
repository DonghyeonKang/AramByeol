import requests

def sendData(msg):
    url='https://hooks.slack.com/services/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'
    data = {'text':msg}
    resp = requests.post(url=url, json=data)
    return resp