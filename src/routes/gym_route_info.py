from src.app import app
from flask import request
from google.cloud import storage
from google.oauth2 import service_account
import os
from datetime import datetime, timedelta

indoor_map = ["maps/indoor_map_generic.png", "maps/indoor_map_generic.png", "maps/indoor_map_generic.png"]
custom_gym_header = ["gym_header/generic_header.png", "gym_header/guelph_atl_center.png", "gym_header/grr_header.png"]

gym_routes = {
    "1": [
        {
            "id": 1,
            "climb_name": "Helicopter",
            "gym_name": "The Guelph Grotto",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
        {
            "id": 2,
            "climb_name": "Helicopter",
            "gym_name": "The Guelph Grotto",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
        {
            "id": 3,
            "climb_name": "Helicopter",
            "gym_name": "The Guelph Grotto",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
    ],
    "2": [
        {
            "id": 1,
            "climb_name": "Helicopter",
            "gym_name": "Guelph Athletics Center",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
        {
            "id": 2,
            "climb_name": "Helicopter",
            "gym_name": "Guelph Athletics Center",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
        {
            "id": 3,
            "climb_name": "Helicopter",
            "gym_name": "Guelph Athletics Center",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
    ],
    "3": [
        {
            "id": 1,
            "climb_name": "Helicopter",
            "gym_name": "Grand River Rocks",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
        {
            "id": 2,
            "climb_name": "Helicopter",
            "gym_name": "Grand River Rocks",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
        },
        {
            "id": 3,
            "climb_name": "Helicopter",
            "gym_name": "Grand River Rocks",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
            "description": "Fun and exciting",
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
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to your service account key file relative to the current directory
    keyfile_path = os.path.join(current_directory, 'gdschackathon2024-422307-aaca36ebdcaa.json')

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
    data = request.json
    gym = data.get('gym')

    # Iterate over each gym in gym_routes dictionary
    for gym in gym_routes:
        image_url = generate_signed_url("grotto/helicopter.png")

        for route in gym_routes[gym]:
            # Add climbPhotoUrl to each JSON object
            route["climb_image_url"] = image_url

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



    