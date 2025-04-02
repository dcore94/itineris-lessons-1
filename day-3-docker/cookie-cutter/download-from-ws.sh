echo "Getting token"
TOKEN=$(curl -X POST $ccpiamurl -d grant_type=refresh_token -d client_id=$ccpclientid -d refresh_token=$ccprefreshtoken | jq -r '."access_token"')

echo Downloading $1 to $2
curl -L $1 -o $2 -H "Authorization: Bearer $TOKEN"

echo "Downloaded"