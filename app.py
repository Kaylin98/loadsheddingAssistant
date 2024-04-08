from flask import Flask, request, make_response
import requests
import os
import json
import urllib.parse
from datetime import datetime

app = Flask(__name__)

def get_today_schedule(json_data):
    today = datetime.now().strftime("%A")
    for day in json_data["schedule"]["days"]:
        if day["name"] == today:
            return day["stages"]
    return None

def filter_passed_times(time_slots):
    current_time = datetime.now().strftime("%H:%M")
    return [time_slot for time_slot in time_slots if time_slot >= current_time]

def format_time_slots(time_slots):
    formatted_times = []
    for slot in time_slots:
        start, end = slot.split("-")
        formatted_times.append(f"from {start} to {end}")
    return formatted_times


@app.route('/webhook', methods=['POST'])
def webhook():
    api_key = os.getenv('ESP_API_KEY')
    request_headers = {'accept': 'application/json', 'Token': api_key}
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    
    answer = ""

    if intent == 'LoadsSchedule':

        status_url = "https://developer.sepush.co.za/business/2.0/status"
        headers = {"Token": api_key}
        
        # Get status information
        status_response = requests.get(status_url, headers=headers)
        if status_response.status_code == 200:
            status_data = status_response.json()
            # Get Eskom stage
            eskom_stage = int(status_data["status"]["eskom"]["stage"])
            
            # Fetch schedule based on today's date
            schedule_url = "https://developer.sepush.co.za/business/2.0/area?id=jhbcitypower3-10-ferndale"
            schedule_response = requests.get(schedule_url, headers=headers)
            
            if schedule_response.status_code == 200:
                schedule_data = schedule_response.json()
                # Get today's schedule
                stages = get_today_schedule(schedule_data)
                if stages:
                    if eskom_stage < len(stages):
                        current_stages = filter_passed_times(stages[eskom_stage])
                        if current_stages:
                            formatted_times = format_time_slots(current_stages)
                            answer = "The next upcoming outages are at " + ", and ".join(formatted_times)
                        else:
                            answer = "No outages scheduled for today."

        return make_response({
            "fulfillmentText": answer,
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses":{
                        "simpleResponses": [
                            {
                                "textToSpeech": answer
                            }
                        ]
                    }
                }
            ],
            "source": "webhook"
        })
    


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')