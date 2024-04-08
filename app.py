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
            schedule_url = "https://developer.sepush.co.za/business/2.0/area?id=jhbcitypower3-10-ferndale&test=current"
            schedule_response = requests.get(schedule_url, headers=headers)
            
            if schedule_response.status_code == 200:
                schedule_data = schedule_response.json()
                # Get today's schedule
                stages = get_today_schedule(schedule_data)
                

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