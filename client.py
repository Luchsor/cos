import requests
import json
from cos_functions import policy_variables

# Define the URL of the REST interface
url = 'http://localhost:5000/create_request'  # Replace with your actual URL



# Create a new policy_variables object
variables = policy_variables(
    subject='CN=tst.a41mgt.local',
    friendly_name='tst.a41mgt.local',
    alternative_names=['tst.a41mgt.local'],
)

# Create the payload
payload = variables.__dict__


# Make the request
response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

# Print the response
print(response.json())