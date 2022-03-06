import requests

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

sql = "insert into order_sum SELECT TUMBLE_ROWTIME(ordertime, INTERVAL '10' SECONDS) AS windowtime, COUNT(*) AS numorders, SUM(totalprice) AS sumtotalprice FROM orders GROUP BY TUMBLE(ordertime, INTERVAL '10' SECONDS);"
sessionCluster = 'sql-editor-previews'
deployName = 'mydeployment'

json_data = {
    'metadata': {
        'displayName': deployName,
    },
    'spec': {
        'sessionClusterName': sessionCluster,
        'template': {
            'spec': {
                'artifact': {
                    'kind': 'SQLSCRIPT',
                    'sqlScript': sql,
                },
            },
        },
        'deploymentTargetId': None,
        'deploymentTargetName': None,
    },
}

response = requests.post('http://localhost:8080/api/v1/namespaces/default/deployments', headers=headers, json=json_data)

json_data = {
    'spec': {
        'state': 'RUNNING',
    },
}

response = requests.patch('http://localhost:8080/api/v1/namespaces/default/deployments/'+deployName, headers=headers, json=json_data)
