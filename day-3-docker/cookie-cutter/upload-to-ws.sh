echo "Getting token"
TOKEN=$(curl -X POST $ccpiamurl -d grant_type=refresh_token -d client_id=$ccpclientid -d refresh_token=$ccprefreshtoken | jq -r '."access_token"')

url="$1/create/FILE"
file=$2
if [ -z "$3" ]; then
    filename=$file
else
    filename=$3
fi

echo "Uploading to $url file $file named as $filename"
curl $url -X POST -H "Authorization: Bearer $TOKEN" -F "name=$filename" -F "file=@$file" -F "description=file $file uploadaded from inside CCP method"

echo "Uploaded"