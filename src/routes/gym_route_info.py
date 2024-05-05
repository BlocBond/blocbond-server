from src.app import app
from flask import request
from google.cloud import storage
from google.oauth2 import service_account
import os
from datetime import datetime, timedelta
import json

indoor_map = [ "maps/indoor_map_generic.png", 
               "maps/indoor_map_generic.png", 
               "maps/indoor_map_generic.png" ]

custom_gym_header = [ "gym_header/generic_header.png", 
                      "gym_header/guelph_atl_center.png", 
                      "gym_header/grr_header.png" ]

gym_routes_arr = { "1": [ "grotto/redholds.png", "grotto/whiteholds.png"], 
                   "2": ["uog/blueholds.png", "uog/redholds.png", "uog/whiteholds.png"],
                   "3": ["grr/blackholds.png", "grr/greenholds.png", "grr/yellowholds.png"], }

map_id_to_folder_name = {
    "1": "grotto",
    "2": "uog",
    "3": "grr"
}

gym_routes = {
    "1": [
        {
            "id": 1,
            "climb_name": "Helicopter",
            "gym_name": "The Guelph Grotto",
            "v_rating": "V3",
            "climb_type": "dyno",
            "hold_type": "crimps",
            "description": "Fun and cool",
        },
        {
            "id": 2,
            "climb_name": "Precise and gentle",
            "gym_name": "The Guelph Grotto",
            "v_rating": "V2",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "Fun and exciting",
        },
    ],
    "2": [
        {
            "id": 1,
            "climb_name": "Who is next",
            "gym_name": "Guelph Athletics Center",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Powerful",
        },
        {
            "id": 2,
            "climb_name": "Why slab or not",
            "gym_name": "Guelph Athletics Center",
            "v_rating": "V5",
            "climb_type": "slab",
            "hold_type": "small or big",
            "description": "Cool climb",
        },
        {
            "id": 3,
            "climb_name": "Spin and more",
            "gym_name": "Guelph Athletics Center",
            "v_rating": "V2",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
    ],
    "3": [
        {
            "id": 1,
            "climb_name": "Why me again?",
            "gym_name": "Grand River Rocks",
            "v_rating": "V5",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Smile and pray",
        },
        {
            "id": 2,
            "climb_name": "Is this a V4",
            "gym_name": "Grand River Rocks",
            "v_rating": "V4",
            "climb_type": "overhang",
            "hold_type": "jugs",
            "description": "Footwork",
        },
        {
            "id": 3,
            "climb_name": "Try me",
            "gym_name": "Grand River Rocks",
            "v_rating": "V2",
            "climb_type": "slab",
            "hold_type": "slopers",
            "description": "Enjoy and relax",
        },
    ],
}

gyms_info = {
    "1": { 
        "id": 1,
        "gym_name": "The Guelph Grotto",
        "logo_image_url": "https://media.licdn.com/dms/image/D560BAQFAsLd-Ma8Akg/company-logo_200_200/0/1693245801216/the_guelph_grotto_logo?e=1723075200&v=beta&t=YafeF7TJL3rT0M3WDD4TXvyfLjVPM71pqGg_IzThdyQ",
        "lat": 43.55212,
        "lng": -80.22461,
    },
    "2": { 
        "id": 2,
        "gym_name": "Guelph Athletics Center",
        "logo_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuHgXWkzSNeT_KzVpQCU36ppnn3vuDcyx96yP0RUl-iw&s",
        "lat": 43.53363,
        "lng": -80.22412,
    },
    "3": { 
        "id": 3,
        "gym_name": "Grand River Rocks",
        "logo_image_url": "https://grandriverrocks.com/wp-content/themes/grand-river-rocks/images/grand-river-rocks-logo.png",
        "lat": 43.47542,
        "lng": -80.52020,
    },
}

def generate_signed_url(file_name_path):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to your service account key file relative to the current directory
    keyfile_path = os.path.join(current_directory, '..', '..', 'resources', 'gdschackathon2024-422307-aaca36ebdcaa.json')

    credentials = service_account.Credentials.from_service_account_file(
        keyfile_path)
    storage_client = storage.Client(credentials=credentials)

    bucket_name = 'route_images'
    bucket = storage_client.bucket(bucket_name)

    # Get a blob (file) from the bucket
    blob = bucket.blob(file_name_path)

    expiration_time = datetime.now() + timedelta(hours=48)
    url = blob.generate_signed_url(expiration=expiration_time) 
    return url

@app.route('/routes', methods=['GET'])
def get_routes():
    gym = str(request.args.get('gym'))

    if gym == "all":
        # return all the routes
        # Iterate over each gym in gym_routes dictionary and add url for the photo

        for gym in gym_routes:
            counter = 0

            for route in gym_routes[gym]:
                image_url = generate_signed_url(gym_routes_arr[gym][counter])
                route["climb_image_url"] = image_url
                counter += 1
    else:
        climbs_to_update = gym_routes.get(gym, [])
       
        counter = 0
        for route in climbs_to_update:
            image_url = generate_signed_url(gym_routes_arr[gym][counter])
            route["climb_image_url"] = image_url
            counter += 1
        
        result = {gym: climbs_to_update}
        print(result)
        return result

    print(gym_routes)
    return gym_routes, 200

@app.route('/gyms', methods=['GET'])
def get_gyms():
    counter = 0
    for gym_id, gym in gyms_info.items():
        url_indoor_map = generate_signed_url(indoor_map[counter])
        url_custom_gym_header = generate_signed_url(custom_gym_header[counter])
        counter += 1

        gym["indoor_map_url"] = url_indoor_map
        gym["url_custom_gym_header"] = url_custom_gym_header

    print(gyms_info)
    return gyms_info, 200

@app.route('/store_climb', methods=['POST'])
def store_climb():
    data = json.loads(request.data.decode('utf-8'))
    # print(data)

    gym_id = data.get('gym_id')
    climb_name = data.get('climb_name')
    gym_name = data.get('gym_name')
    v_rating = data.get('v_rating')
    climb_type = data.get('climb_type')
    hold_type = data.get('hold_type')
    description = data.get('description')
    image_name = data.get('image_name')

    # Do something about the photo
    print(image_name[:32])

    # Upload the photo to GCS Bucket

    # construct new json object - climb_info 
    climb_info = {
        "climb_name": climb_name,
        "gym_name": gym_name,
        "v_rating": v_rating,
        "climb_type": climb_type,
        "hold_type": hold_type,
        "description": description
    }

    if gym_id in gym_routes_arr and gym_id in gym_routes:
        gym_routes_arr[gym_id].append(map_id_to_folder_name[gym_id] + "/" + image_name)
        gym_routes[gym_id].append(climb_info)
    else:
        print(f"ID '{gym_id}' not found. Can't store the climb")
        return "Failure. Can't store the climb", 400

    print(gym_routes)
    return "Success", 200
