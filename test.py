import requests

def sendData(day_mornings, day_lunches, day_dinners):
    text_morning = []
    text_lunch = []
    text_dinner = []

    token = "xoxb-3707654943089-3694992446515-iUBiqQvZIYjWS2bb4Oi8vKuO"
    channel = "#aram_data"

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
        requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token},
            data={"channel": channel,"text": i})