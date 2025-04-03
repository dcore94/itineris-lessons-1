from PIL import Image, ImageDraw, ImageFont
import requests
import json
import sys
import os

face_service = sys.argv[1]
threshold = 0.6
if len(sys.argv) == 3:
    threshold = float(sys.argv[2])
input_image_file = "picture"
source_embeddings_file = "embeddings.json"
target_embeddings_folder = "target_embeddings"

font = ImageFont.truetype("DejaVuSans.ttf", size=25)
image = Image.open(input_image_file)
draw = ImageDraw.Draw(image)

# Extract target embeddings
print("Extracting source embeddings...")
sources = json.load(open(source_embeddings_file))
source_embeddings = [source["embedding"] for source in sources]
print("Extracted", len(source_embeddings), "embeddings")

for target_file in os.listdir(target_embeddings_folder):
    fpath = os.path.join(target_embeddings_folder, target_file)
    target = json.load(open(fpath))
    label = target[0]["label"]
    print("Extracted", len(target), "embeddings for target with label", label)

    for tgt in target:
        embedding = tgt["embedding"]
        print("Calling face service for comparing source with target", label)
        body = { "sources" : source_embeddings, "target" : embedding, "threshold" : threshold}
        resp = requests.post(face_service + "/compare", json = body)
        if resp.ok:
            matches = resp.json()
            for i in range(len(matches)):
                if matches[i]["match"]:
                    box = tuple(sources[i]["box"])
                    color = "red" if matches[i]["similarity"] < 0.9 else "green"
                    draw.rectangle(box, outline=color, width=3)
                    draw.text((box[0], box[3]), label + " (" + str(round(100 * matches[i]["similarity"])) + "%)", fill="blue", font=font)
        else:
            print("Skipping because of error in", label, resp.text)
    

# Save or display the edited image
labelled_image = "output.jpeg"
print("Saving image at " + labelled_image)
image.save(labelled_image)