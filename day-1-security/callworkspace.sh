WS="https://api.d4science.org/workspace"
QUERY=
URL="$WS/$QUERY"

echo "insert token:"
read token

echo "Calling $URL"
curl -X GET --location $URL --header "Authorization: Bearer $token" 
