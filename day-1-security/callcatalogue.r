library(httr)
library(jsonlite)
library(rstudioapi)

# Init
user = 'your_username'
context = '/d4science.research-infrastructures.eu/FARM/ITINERIS_Training-Platform'
auth_ep = 'https://accounts.d4science.org/auth/realms/d4science/protocol/openid-connect/token'
client_id = 'itineris.d4science.org'

getToken <- function() {
  body = list('grant_type'='password', 'scope'=paste('d4s-context',context, sep=':'), 'client_id'=client_id, 'username'=user, 'password'=pwd)
  res = POST(auth_ep, body=body, encode=c('form'), add_headers(c('Content-Type' = 'application/x-www-form-urlencoded')))
  jwt = fromJSON(content(res, 'text'))
  return (jwt)
}

# Auth code
pwd = clear('Password to login')
jwt = getToken()

catalogue = "https://api.d4science.org/catalogue"
query = "items?limit=10&offset=0"
url = paste(catalogue, query, sep="/")

resp = GET(url, add_headers(c('Authorization' = paste('Bearer', jwt["access_token"], sep=' '))))
print(fromJSON(content(resp, 'text')))