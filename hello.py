import os
import json
import requests
os.environ["REPLICATE_API_TOKEN"]="5e8542a3f24574d987db5000c484a186cc2a3807"
from flask import Flask, render_template
from concurrent.futures import ThreadPoolExecutor
import replicate
from io import BytesIO
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
from fb_sketch import animatify, ANIMATIONS

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/draw")
def script():
    return render_template("draw.html")
from flask import request
import base64
from threading import Thread
@app.route("/save", methods=["POST"])
def save():
    header = "data:image/png;base64,"
    from PIL import Image
    data = request.data[len(header):]
    data = base64.b64decode(data)
    
    print(data[:10])
    open("lol.png", "wb").write(data)

    model = replicate.models.get("stability-ai/stable-diffusion-img2img")
    version = model.versions.get("15a3689ee13b0d2616e98820eca31d4c3abcd36672df6afce5cb6feb1d66087d")
    # https://replicate.com/stability-ai/stable-diffusion-img2img/versions/15a3689ee13b0d2616e98820eca31d4c3abcd36672df6afce5cb6feb1d66087d#input
    subinputs = [
    {
        'prompt_strength': 0.4,
        'prompt': "human figure with 2 arms and 2 legs on white background, 2d, drawing, children's book",
    },
    {
        'prompt_strength': 0.8,
        'prompt': "photorealistic human figure with 2 arms and 2 legs",
    },

    ]
    inputs = {
        # Input prompt
        'prompt': "human figure with 2 arms and 2 legs on white background, 2d, drawing, children's book",

        # The prompt NOT to guide the image generation. Ignored when not using
        # guidance
        # 'negative_prompt': ...,

        # Inital image to generate variations of.
        'image': BytesIO(data),

        # Prompt strength when providing the image. 1.0 corresponds to full
        # destruction of information in init image
        'prompt_strength': 0.7,

        # Number of images to output. Higher number of outputs may OOM.
        # Range: 1 to 8
        'num_outputs': 1,

        # Number of denoising steps
        # Range: 1 to 500
        'num_inference_steps': 25,

        # Scale for classifier-free guidance
        # Range: 1 to 20
        'guidance_scale': 7.5,

        # Choose a scheduler.
        'scheduler': "DPMSolverMultistep",

        # Random seed. Leave blank to randomize the seed
        # 'seed': ...,
    }

    pool = ThreadPoolExecutor(2)
    inputs = [{**inputs, **si} for si in subinputs]

    # https://replicate.com/stability-ai/stable-diffusion-img2img/versions/15a3689ee13b0d2616e98820eca31d4c3abcd36672df6afce5cb6feb1d66087d#output-schema
    outputs = list(pool.map(lambda inp: version.predict(**inp), inputs))
    urls = [x[0] for x in outputs]
    print("Got url", urls)
    urls = list(pool.map(make_anim, urls))
    print("Got movie url", urls)
    # print(url)
    return json.dumps(urls)

def make_anim(url):
    print("Downloading", url)
    image_resp = requests.get(url)
    open("image.png", "wb").write(image_resp.content)
    url = animatify(image_resp.content, ANIMATIONS[0])
    return url
