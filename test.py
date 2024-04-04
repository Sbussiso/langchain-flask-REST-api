import requests, json


prompt = input("Enter Prompt: ")

#endpoint and serialization
url = 'http://127.0.0.1:5000/chat'
data = json.dumps({'prompt': prompt})

#send and save POST
response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

#check success
if response.status_code == 200:
    #Parse JSON response
    response_data = response.json()
    print(response_data)
else:
    print("Error:", response.status_code)