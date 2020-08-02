"""
import requests

# from requests.auth import HTTPBasicAuth


headers = {
    "Authorization": "key=AIzaSyBXTqrBv8wH6qW0BrOIeE7c1wfGbxghlS4"
}  # Content-Type": "application/json",
token = "fnW2sId-8fI:APA91bHn8ol60dqGk1KkZYQXLj39FZVGZ_2nNKMFCzVEWVfLybQC13MXUX0N7hGyKz_RdWmx7CA9nzQVSfD_K89ytP4ZDV-cYl91oLq8GjUXa494A1kz59iKae1aqq3EA9iL-l5_duAQ"
URL = f"https://iid.googleapis.com/iid/info/{token}"
res = requests.get(URL, headers=headers)
# res = requests.get(
#    URL, auth=HTTPBasicAuth("key", "AIzaSyBXTqrBv8wH6qW0BrOIeE7c1wfGbxghlS4")
# )
print(res)
"""
import requests

headers = {
    "Authorization": "AIzaSyBXTqrBv8wH6qW0BrOIeE7c1wfGbxghlS4",
    "Content-Type": "application/json",
}  # Content-Type": "application/json",

token = "fe3-nuGiP9A:APA91bGktPHqVY4TVMMQBRM-fQvh8wOyxPc1v8LByZ7NMwdpUKu9QQ2ttqWrZoEDoQ8xE8z-5gkyE6sxeyrTHVFgmnW_06xWloT9T-pzPS6n0Vox2ceXt54pCZJIEJ71RTa61XO_uYg3"
URL = "https://fcm.googleapis.com/fcm/send"

res = requests.post(URL, data={"registration_ids": token}, headers=headers)

print(res)
