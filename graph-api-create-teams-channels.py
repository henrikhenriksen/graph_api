import requests
import json

# Variables
tenant_id = '' #Entra ID Tenant ID
client_id = '' #
client_secret = '' #secret
group_id = ''  # The ID of the Teams group where you want to create channels

# URLs
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
graph_url = f'https://graph.microsoft.com/v1.0/teams/{group_id}/channels'

# Get access token
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
}

token_r = requests.post(token_url, data=token_data)

if token_r.status_code == 200:
    token = token_r.json().get('access_token')
    if token and '.' in token:  # Check if the token format looks correct
        print("Token obtained successfully.")
    else:
        print("Token format is incorrect or missing.")
else:
    print("Failed to obtain token. Status code:", token_r.status_code)
    print("Response:", token_r.text)
    exit()  # Exit if we can't get a valid token

# Proceed with the rest of the script...

# Headers for Graph API request
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Create 1000 channels
for i in range(1, 1000):
    channel_name = f'Channel {i}'
    channel_description = f'This is channel number {i}'

    # Payload for creating a new channel
    payload = {
        'displayName': channel_name,
        'description': channel_description,
        'membershipType': 'standard',  # standard or private
    }

    # POST request to create a new channel
    response = requests.post(graph_url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        print(f'Successfully created {channel_name}')
    else:
        print(f'Failed to create {channel_name}. Response: {response.text}')
        break  # Exit the loop if a creation fails to avoid unnecessary requests