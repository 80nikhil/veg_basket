import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import os
from firebase_admin import messaging

# fire_cred_json = {
        
#         }
# cred = credentials.Certificate(fire_cred_json)
# firebase_admin.initialize_app(cred)

def send_firebase_notification(tokens, title, body, data=None):
    """
    Fallback if send_multicast is unavailable.
    """
    success = 0
    failure = 0
    responses = []

    for token in tokens:
        message = messaging.Message(
            token=token,
            notification=messaging.Notification(title=title, body=body),
            data=data or {}
        )
        try:
            resp = messaging.send(message)
            responses.append({"token": token, "response": resp, "success": True})
            success += 1
        except Exception as e:
            responses.append({"token": token, "error": str(e), "success": False})
            failure += 1

    return {"success": success, "failure": failure, "responses": responses}