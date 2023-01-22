from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/draw")
def script():
    return render_template("draw.html")


@app.route("/stable-difussion", methods=["POST"])
def generate_image():
    model = replicate.models.get("stability-ai/stable-diffusion-img2img")
    version = model.versions.get("15a3689ee13b0d2616e98820eca31d4c3abcd36672df6afce5cb6feb1d66087d")

    # https://replicate.com/stability-ai/stable-diffusion-img2img/versions/15a3689ee13b0d2616e98820eca31d4c3abcd36672df6afce5cb6feb1d66087d#input
    inputs = {
        # Input prompt
        'prompt': "human figure with 2 arms and 2 legs on white background",

        # The prompt NOT to guide the image generation. Ignored when not using
        # guidance
        # 'negative_prompt': ...,

        # Inital image to generate variations of.
        'image': open("static/figure.png", "rb"),

        # Prompt strength when providing the image. 1.0 corresponds to full
        # destruction of information in init image
        'prompt_strength': 0.4,

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

    # https://replicate.com/stability-ai/stable-diffusion-img2img/versions/15a3689ee13b0d2616e98820eca31d4c3abcd36672df6afce5cb6feb1d66087d#output-schema
    output = version.predict(**inputs)
    print(output)
