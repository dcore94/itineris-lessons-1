#!/bin/bash

face_service_url=$1
image_url=$2
label=$3
embeddings_folder_url=$4

echo Initializing. Downloading image from $image_url to file picture
./download-from-ws.sh $image_url picture

echo Executing. 

echo Calling face service at $face_service_url with image picture and storing measures in embeddings.json
curl -X POST $face_service_url/process -F "image=@picture" -o embeddings.json

echo Running python script to enrich image picture and labeling with $label and storing embeddings at $embeddings_folder_url
python3 train.py $label

cp picture "$label.jpeg" embeddings.json labelled_embeddings.json /ccp_data

./upload-to-ws.sh $embeddings_folder_url labelled_embeddings.json "$label"_embeddings.json