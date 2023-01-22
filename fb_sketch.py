# %%
import json
import requests

ANIMATIONS =[
    "running_jump",
    "wave_hello_3",
    "hip_hop_dancing",
    "box_jump",
    "boxing",
    "catwalk_walk",
    "dab_dance",
    "dance",
    "dance001",
    "dance002",
    "floating",
    "flying_kick",
    "happy_idle",
    "hip_hop_dancing2",
    "hip_hop_dancing3",
    "jab_cross",
    "joyful_jump_l",
    "jump",
    "jump_attack",
    "jump_rope",
    "punching_bag",
    "run",
    "run_walk_jump_walk",
    "shoot_gun",
    "shuffle_dance",
    "skipping",
    "standard_walk",
    "walk_punch_kick_jump_walk",
    "walk_sway",
    "walk_swing_arms",
    "waving_gesture",
    "zombie_walk",
]
def upload(file):
    resp = requests.post("https://production-sketch-api.metademolab.com/upload_image", files={"file": file})
    assert resp.ok
    uuid = resp.text
    r = requests.post("https://production-sketch-api.metademolab.com/set_consent_answer", data={
        "uuid": uuid,
        "consent_response": 1,
    })

    return uuid

def get_bounding_box_coordinates(uuid):
    resp = requests.post("https://production-sketch-api.metademolab.com/get_bounding_box_coordinates", data={
        "uuid": uuid,
    })
    assert resp.ok
    return resp.json()

def set_bounding_box_coordinates(uuid, bounding_box_coordinates):
    resp = requests.post(
        'https://production-sketch-api.metademolab.com/set_bounding_box_coordinates',
        data={
            "uuid": uuid,
            "is_scenes": "false",
            "bounding_box_coordinates": json.dumps(bounding_box_coordinates),
        }
    )
    assert resp.ok, f"set_bounding_box_coordinates failed {resp.text}"
    assert resp.ok

def get_mask(uuid):
    resp = requests.post("https://production-sketch-api.metademolab.com/get_mask", 
    data={
        "uuid": uuid,
    })
    assert resp.ok, "get_mask failed"
    return resp.content

def set_mask(uuid, mask):
    resp = requests.post("https://production-sketch-api.metademolab.com/set_mask",
    data={
        "uuid": uuid,
    },
    files={"file": mask})

    assert resp.ok, "set_mask failed"

def get_joint_locations(uuid):
    resp = requests.post("https://production-sketch-api.metademolab.com/get_joint_locations_json", data={
        "uuid": uuid,
    })
    assert resp.ok, "get_joint_locations failed"
    joints = resp.json()
    return joints

def set_joint_locations(uuid, joints):
    resp = requests.post("https://production-sketch-api.metademolab.com/set_joint_locations_json", data={
        "uuid": uuid,
        "joint_location_json": json.dumps(joints),
    })
    assert resp.ok, "set_joint_locations failed"
    return resp

def get_animation(uuid, animation):
    resp = requests.post("https://production-sketch-api.metademolab.com/get_animation", data={
        "uuid": uuid, 
        "animation": animation,
        "create_webp": True,
    })

    assert resp.ok, "get_animation failed"
    anim_id = resp.text
    return f"https://production-sketch-video.metademolab.com/{anim_id}/{animation}.mp4"

def get_cropped_image(uuid):
    resp = requests.post("https://production-sketch-api.metademolab.com/get_cropped_image", data={
        "uuid": uuid,
    })
    assert resp.ok
    return resp.content
import random
def run_test():
    animation = random.choice(ANIMATIONS)
    animation_url = animatify(open("./image.jpg", "rb"), animation)
    print("Downloading animation...")
    r = requests.get(animation_url, stream=True)
    open(f"{animation}.mp4", "wb").write(r.content)

def animatify(image, animation):
    print("Uploading...")
    uuid = upload(image)

    print("Setting up coords...")
    coords = get_bounding_box_coordinates(uuid)
    set_bounding_box_coordinates(uuid, coords)
    
    # not needed!
    # print("Setting up mask...")
    # mask = get_mask(uuid)
    # set_mask(uuid, mask)

    print("Setting up joints...")
    joints = get_joint_locations(uuid)
    set_joint_locations(uuid, joints)

    print("Getting animation...")
    import random
    animation_url = get_animation(uuid, animation)
    print(animation_url)
    return animation_url



if __name__ == "__main__":
    run_test()
