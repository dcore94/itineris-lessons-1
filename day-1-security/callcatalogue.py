import requests
import getpass

context = "/d4science.research-infrastructures.eu/FARM/ITINERIS_Training-Platform"
clientid = "itineris.d4science.org"
user = "your_username"
pwd = getpass.getpass("Insert password: ")
iam = "https://accounts.d4science.org/auth/realms/d4science/protocol/openid-connect/token"


#Auth related functions
def getToken():
    logindata = { "grant_type" : "password", "client_id" : clientid, "username" : user, "password" : pwd, "scope" : "d4s-context:" + context }
    loginheaders = { "Content-Type" : "application/x-www-form-urlencoded"}
    resp = requests.post(iam, data=logindata, headers=loginheaders)
    print(resp)
    jwt = resp.json()
    return jwt

def refreshToken(jwt):
    logindata = { "grant_type" : "refresh_token", "client_id" : clientid, "refresh_token" : jwt["refresh_token"]}
    loginheaders = { "Accept" : "application/json", "Content-Type" : "application/x-www-form-urlencoded"}
    resp = requests.post(iam, data=logindata, headers=loginheaders)
    print(resp)
    jwt = resp.json()
    return jwt

# Get valid token for context
jwt = getToken()
accesstoken = jwt["access_token"]

catalogue = "https://api.d4science.org/catalogue"
query = "items?limit=10&offset=0"
url = catalogue + "/" + query

resp = requests.get(url, headers={"Authorization" : "Bearer " + accesstoken})
print(resp)
print(resp.json())

print(refreshToken(jwt))
