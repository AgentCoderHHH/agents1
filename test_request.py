import requests
import json

url = "http://localhost:3001/execute"
payload = {
    "topic": "i would now like to create a new agent. may be few for reporting and analytics. we have a website, and we have twitter. for website data and google analytics i will to make an agent that will read data from the google sheet and report the data in presentable manner. | for twitter i want the agent to go and grab from google sheet which is in a json format i guess your job now to make detailed plan of differetn agent needed for these task. e.g. for fetching agents whcih are differetn, digest the data agent, see the best possible metrics needed for that field and stay on topic, presenting agent which will code frontend and show to user agent, alert agent to notify devs seperate community seperate or other parties ( mention which channel?? telegram or?? ) and may be a lot more process of agents. please brainstrom. get the data and again provide the final defination of the agents i need along with mermaid of the new agents u added. feel free to use the current agents which we have when needed.",
    "reasoning_effort": "high"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2)) 