import requests

def slackCommit(msg):
    url='https://hooks.slack.com/services/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'
    payload={"text": msg}
    resp = requests.post(url=url, json=payload)
    return resp

def sendData(day_mornings, day_lunches, day_dinners):
    slackCommit("******************* 이번주 식단 *******************")
    text_morning = []
    text_lunch = []
    text_dinner = []

    for i in range(len(day_mornings)):
        text_morning.append(" ".join(day_mornings[i]))

    for i in range(len(day_lunches)):
        text_lunch.append(" ".join(day_lunches[i]))

    for i in range(len(day_dinners)):
        text_dinner.append(" ".join(day_dinners[i]))

    week = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    text = []
    for i in range(7):
        text.append('==================')
        text.append(week[i])
        text.append('아침')
        text.append(text_morning[i])
        text.append('점심')
        text.append(text_lunch[i])
        text.append('저녁')
        text.append(text_dinner[i])
        for i in text:
            slackCommit(i)
        text = []
