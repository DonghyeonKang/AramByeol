import slack 
import json
import requests

def post_to_slack(message):
    webhookUrl = 'https://hooks.slack.com/services/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'
    print(message)
    data = [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': message}}]
    slackData = json.dumps({'blocks': data})

    response = requests.post(
        webhookUrl, data=slackData,
        headers={'Content-Type':'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )



post_to_slack("asdfahsdudsfuhafaihusfiuasdniufsadniufdsn")
