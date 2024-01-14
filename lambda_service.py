import boto3
import json
import urllib.parse
import http.client
import boto3
from botocore.exceptions import NoCredentialsError


teams_webhook = ""
teams_webhook2 = ""
ms_team_connector_name=""
def cpresigned_url(bucket_name, object_name, expiration=43200):

    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response



def lambda_handler(event, context):
    if event['Records'][0]['eventName'].startswith('ObjectCreated:'):
        s3_event = event['Records'][0]['s3']
        bucket_name = s3_event['bucket']['name']
        object_key = urllib.parse.unquote_plus(s3_event['object']['key'])

        expiration_time = 43200
        presigned_url = cpresigned_url(bucket_name, object_key, expiration_time)

        teams_webhook_url = teams_webhook

        teams_payload = {
            "text": "This Error Generated",
            "sections": [
                {
                    "activityTitle": object_key,
                    "activityImage": presigned_url,
                    "potentialAction": [
                        {
                            "@type": "OpenUri",
                            "name": "View Full Size",
                            "targets": [
                                {
                                    "os": "default",
                                    "uri": presigned_url
                                }
                            ]
                        }
                    ]
                }
            ]
        }


        conn = http.client.HTTPSConnection(ms_team_connector_name)
        conn.request("POST", teams_webhook2, json.dumps(teams_payload))
        response = conn.getresponse()

        print(f"Response Status: {response.status}")
        print(f"Response Reason: {response.reason}")
        print(f"Response Body: {response.read().decode()}")

        if response.status != 200:
            print(f"Failed to send message to Microsoft Teams. Status code: {response.status}")
        else:
            print("Message sent successfully to Microsoft Teams.")

    else:
        print("Skipping processing. Event is not a new object creation event.")

    return {
        'statusCode': 200,
        'body': json.dumps('Function executed successfully!')
    }
