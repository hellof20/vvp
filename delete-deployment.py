import requests
import time

deployName = 'mydeployment'

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'Origin': 'http://localhost:8080',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'http://localhost:8080/app/',
    'Accept-Language': 'en-US,en;q=0.9',
}

json_data = {
    'spec': {
        'state': 'CANCELLED',
    },
}

response = requests.patch('http://localhost:8080/api/v1/namespaces/default/deployments/'+deployName, headers=headers, json=json_data)

while True:
    response = requests.get('http://localhost:8080/api/v1/namespaces/default/deployments/'+deployName, headers=headers)
    time.sleep(2)
    state = response.json()['status']['state']
    if state == 'CANCELLED':
        break
    print('waiting deploy to be cancelled')

response = requests.delete('http://localhost:8080/api/v1/namespaces/default/deployments/'+deployName, headers=headers)
print('the deployment has been deleted')
