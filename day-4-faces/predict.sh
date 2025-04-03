#!/bin/bash

face_service_url=$1
image_url=$2
embeddings_folder_url=$3

if [ -z "$4" ]; then
    threshold="0.7"
else
    threshold=$4
fi

echo Initializing. Downloading image from $image_url to file picture
./download-from-ws.sh $image_url picture

echo Initializing. Downloading embeddings dataset from $embeddings_folder_url to folder target_embeddings
./download-from-ws.sh $embeddings_folder_url target_embeddings.zip
unzip -jd target_embeddings target_embeddings.zip 

echo Executing. 

echo Calling face service at $face_service_url with image picture and storing measures in embeddings.json
curl -X POST $face_service_url/process -F "image=@picture" -o embeddings.json

echo Running python script to enrich image picture storing enriched image output.jpeg
python3 predict.py $face_service_url $threshold

cp picture output.jpeg embeddings.json /ccp_data