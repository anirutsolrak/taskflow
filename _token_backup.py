import msal

CLIENT_ID = "37f64015-d93b-4840-ac56-9e857149a10e"

SCOPES = ["Tasks.ReadWrite", "Group.ReadWrite.All", "User.Read"]

app = msal.PublicClientApplication(CLIENT_ID, authority="https://login.microsoftonline.com/common")

flow = app.initiate_device_flow(scopes=SCOPES)
print(flow["message"])

result = app.acquire_token_by_device_flow(flow)

if "access_token" in result:
    print("\n✅ TOKEN:")
    print(result["access_token"])
else:
    print("Erro:", result.get("error_description"))