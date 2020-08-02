from firebase_admin import messaging
from firebase_admin import credentials
from firebase_admin import initialize_app

cred = credentials.Certificate("fir-test-d20b3-firebase-adminsdk-u3j7c-f95f9b1e7d.json")
initialize_app(cred)

registration_token = "cY3JX6C99ExWhJWuINhnBn:APA91bHA9f_JFAJq9T2MC0LBxpsr0T_YB7g4nXzJOgS6gKMhm7pGWHcnC9JoVbTOX8ph_HDuN6Pj4FF3aS9nkTkM08XwaDC661bF23bvtZu_7H5_iKI6AChJtkK8ZGein4B13mrF-rfr"

message = messaging.Message(
    apns=messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(
                alert=messaging.ApsAlert(title="test", body="페이지 변경 감지!",),
                badge=1,
                sound=messaging.CriticalSound(name="default",),
            ),
        ),
    ),
    token=registration_token,
)

response = messaging.send(message)
print("Successfully sent message:", response)
