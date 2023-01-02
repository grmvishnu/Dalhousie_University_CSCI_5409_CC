import json

def lambda_handler(event, context):
    if 'email' in event and 'message' in event:
        emailId = event['email']
        text = event['message']
        if "account" in text or "password" in text and emailId != "rhawkey@dal.ca":
            tier = "Tier1"
        elif "computer" in text or "laptop" in text or "printer" in text and emailId != "rhawkey@dal.ca":
            tier = "Tier2"
        elif "rhawkey@dal.ca" in emailId:
            tier = "Tier3"
        else:
            tier = "Unknown"
        return {
            'statusCode': 200,
            'value': tier,
            'email': emailId,
            'textToPass': text
        }
    return {
        'statusCode': 400,
        'error': 'Invalid parameters.'
    }