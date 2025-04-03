from PIL import Image, ImageDraw, ImageFont
import json
import sys

input_image_file = "picture"
label = sys.argv[1]
embeddings_file = "embeddings.json"
labelled_embeddings_file = "labelled_embeddings.json"


# Open the image file
image = Image.open(input_image_file)
embeddings = json.load(open(embeddings_file))

font = ImageFont.truetype("DejaVuSans.ttf", size=25)
draw = ImageDraw.Draw(image)

for m in embeddings:
    box = tuple(m["box"])
    color = "red" if m["confidence"] < 0.9 else "green"
    draw.rectangle(box, outline=color, width=3)
    draw.text((box[0], box[3]), label, fill="cyan", font=font)
    m["label"] = label

# Save or display the edited image
labelled_image = label + ".jpeg"
print("Saving image at " + labelled_image)
image.save(labelled_image)

print("Saving back labelled embeddings at ", labelled_image)
json.dump(embeddings, open(labelled_embeddings_file, "w"))