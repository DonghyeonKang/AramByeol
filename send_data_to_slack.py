import requests

def sendData(text):
    token = "xoxb-3707654943089-3694992446515-iUBiqQvZIYjWS2bb4Oi8vKuO"
    channel = "#aram_data"

    for i in text:
        requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token},
            data={"channel": channel,"text": i})