#!/usr/bin/python3

# The script is to initiate a discovery based on location.
# The devices dicoveried will be assign to the appropriate site on DNAC.
# Usage: python3 vnhchm01_discover.py


from requests.auth import HTTPBasicAuth
import json
import requests
import time
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# URL for DNAC server
BASE_URL = 'https://10.204.0.75'

# URLs for API call
AUTH_URL = '/dna/system/api/v1/auth/token'
SITE_URL = '/dna/intent/api/v1/site'
DISCOVERY_URL = '/dna/intent/api/v1/discovery'
DISCOVERY_DEVICE_URL = '/dna/intent/api/v1/discovery/{discovery_id}/network-device'
ASSIGN_DEVICE_URL = '/dna/intent/api/v1/assign-device-to-site/${site_id}/device'
TASK_BY_ID_URL = '/dna/intent/api/v1/task/{task_id}'

#TODO: Request API token
def get_token():
    token = requests.post(
        BASE_URL + AUTH_URL,
        auth=HTTPBasicAuth(username='d.dinh', password='T@0khongbiet042024'),
        headers={'Content-type': 'application/json'},
        verify=False
    )
    data = token.json()
    return data['Token']

#TODO: Initiate Discovery task
def create_discovery(discovery_parameters, token):
    response = requests.post(
        BASE_URL + DISCOVERY_URL,
        headers={
            'X-Auth-Token': token,
            'Content-type': 'application/json'
        },
        json=discovery_parameters,
        verify=False
    )
    return response.json()['response']

#TODO: Get the ID of Discovery task
def get_task(task_id, token):
    response = requests.get(
        BASE_URL + TASK_BY_ID_URL.format(task_id=task_id),
        headers={
            'X-Auth-Token': token,
            'Content-type': 'application/json'
        },
        verify=False      
    )
    return response.json()['response']

#TODO: Collect the device information from discovery
def get_discovery_devices(discover_id, token):
    response = requests.get(
        BASE_URL + DISCOVERY_DEVICE_URL.format(discover_id=discover_id),
        headers={
            'X-Auth-Token': token,
            'Content-type': 'application/json'
        },
        verify=False      
    )
    return response.json()['response']

#TODO: Assign devices to Site
def assign_device_to_site(site_id, devices, token):
    response = requests.post(
        BASE_URL + ASSIGN_DEVICE_URL.format(site_id=site_id),
        headers={
            'X-Auth-Token': token,
            'Content-type': 'application/json'
        },
        json=devices,
        verify=False        
    )
    return response.json()

if __name__ == "__main__":
    token = get_token()

    # Define the parameters for Discovery of Ho Chi Minh Office
    discovery_parameters = {
        "name": "Discover Ho Chi Minh Office by API",
        "discoveryType": "CDP",
        "cdpLevel": "16",
        "ipAddressList": "10.148.253.1",
        "protocolOrder": "ssh",
        "timeOut": 5,
        "retryCount": 3,
        "globalCredentialIdList": [
            "e599817b-3e5a-4b94-b7d8-4557c703fb1c",
            "1d6a06fe-4894-4724-b918-99d7eaf2a1dd"
        ],
        "snmpUserName": "snmpv3user",
        "snmpVersion": "v3",
        "netconfPort": "830",
        "preferredMgmtIPMethod": "UseLoopBack"
    }

    # Initiate the discovery and output response
    discovery = create_discovery(discovery_parameters, token)
    task_id = discovery['taskId']
    print("Discovery response:", json.dumps(discovery, indent=4))

    # Timing the process for 600s
    print("\nWaiting 600 seconds for discovery to be created...")
    time.sleep(600)

    # Examine the information of discovery task
    task_info = get_task(task_id, token)
    print("Task information:", json.dumps(task_info, indent=4))

    discovery_id = task_info['progress']
    print("Discovery ID:", json.dumps(discovery_id, indent=4))
    
    # Timing the process for 1800s
    print('\nWaiting 1800 seconds for discovery to end...')
    time.sleep(1800) 

    # Collect the devices from discovery task
    discovery_devices = get_discovery_devices(discovery_id, token)
    print("Discoveried devices:", json.dumps(discovery_devices, indent=4))

    # Make the list of devices to be added to specific site
    device_ips = []
    for device in discovery_devices:
        device_ips.append({'ip': device['managementIpAddress']})  
    site_devices = {'device': device_ips}
    print("List of devices to be added by IP address:", json.dumps(site_devices, indent=4))

    # Specify the site_id of Ho Chi Minh Office
    site_id = "d5133724-78af-4054-a772-b1387796b5a8"
    assign_device = assign_device_to_site(site_id, site_devices, token)
    print("Assigning devices response:", json.dumps(assign_device, indent=4)) 