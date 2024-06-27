from src.app import app
from flask import request
from google.cloud import storage
from google.oauth2 import service_account
import os
from datetime import datetime, timedelta
import json
import base64
import random

indoor_map = [ "maps/indoor_map_generic.png", 
               "maps/indoor_map_generic.png", 
               "maps/indoor_map_generic.png", 
               "maps/indoor_map_generic.png", 
               "maps/indoor_map_generic.png",
               "maps/indoor_map_generic.png" ]

custom_gym_header = [ "gym_header/generic_header.png", 
                      "gym_header/guelph_atl_center.png", 
                      "gym_header/grr_header.png",
                      "gym_header/generic_header.png",
                      "gym_header/generic_header.png",
                      "gym_header/generic_header.png"
                    ]

gym_routes_arr = { "1": ["grotto/Messenger_creation_b2719286-eba7-4689-84a5-c59da129dff9.jpeg", "grotto/Messenger_creation_1bb2cd8b-bb68-46c7-8a63-52aff8a9aec8.jpeg", "grotto/Messenger_creation_101e8f27-ce80-44d5-aea2-104384bdd6a4.jpeg", "grotto/Messenger_creation_332e9ea7-a561-4558-8a0c-e12252f9d4fa.jpeg", "grotto/Messenger_creation_94d617db-6c14-4fc4-b594-6f627aa9790e.jpeg", "grotto/Messenger_creation_48d840f6-b219-4f5d-9cac-1f911461c25b.jpeg", "grotto/Messenger_creation_11b0ee40-4e39-4932-be63-3dbb3050694c.jpeg", "grotto/Messenger_creation_854246e7-a261-40c1-ad54-b47c42ea182c.jpeg", "grotto/Messenger_creation_ab36cbe0-7608-4caa-b87b-d24eeec5ccb9.jpeg", "grotto/Messenger_creation_553b1f6f-ed30-4503-b1fe-aa3ad7623473.jpeg", "grotto/Messenger_creation_5bb0791b-1ca4-4bd0-8d1a-9efc354cf85f.jpeg", "grotto/Messenger_creation_e3ab10c6-0b68-4b89-a264-b0f1eeebaea8.jpeg", "grotto/Messenger_creation_b9732a6d-49c3-4cc2-af14-a6a37d156565.jpeg", "grotto/Messenger_creation_be0eb2b6-f0c5-4936-aa29-a8dc1ca5ba2b.jpeg", "grotto/Messenger_creation_91cc5597-cd21-4171-b572-75bd911d0f41.jpeg", "grotto/Messenger_creation_c4f710f9-c2a3-4f27-914a-8473c91ffbb3.jpeg", "grotto/Messenger_creation_09b1b47b-9b8d-4fd6-a407-2ee754bb4d37.jpeg"], 
                   "2": [],
                   "3": ["grr/Messenger_creation_f53f4222-5d5c-4ddc-b3be-8bd94516bd40.jpeg", "grr/Messenger_creation_2806c70d-bb08-425a-af05-dc7bac3cfe81.jpeg"],
                   "4": ["gneiss-banks/20240625_203638.jpg", "gneiss-banks/20240625_203611.jpg", "gneiss-banks/20240625_203559.jpg", "gneiss-banks/20240625_203217.jpg", "gneiss-banks/20240625_203607.jpg", "gneiss-banks/20240625_203616.jpg", "gneiss-banks/20240625_203614.jpg", "gneiss-banks/20240625_203539.jpg", "gneiss-banks/20240625_203513.jpg", "gneiss-banks/20240625_203525.jpg", "gneiss-banks/20240625_203244.jpg", "gneiss-banks/20240625_203537.jpg", "gneiss-banks/20240625_203455.jpg", "gneiss-banks/20240625_203454.jpg", "gneiss-banks/20240625_203235.jpg", "gneiss-banks/20240625_203623.jpg", "gneiss-banks/20240625_203636.jpg", "gneiss-banks/20240625_203543.jpg"],
                   "5": ["gneiss-hill/20240622_220446.jpg", "gneiss-hill/20240622_220445.jpg", "gneiss-hill/20240622_220451.jpg", "gneiss-hill/20240622_220436.jpg", "gneiss-hill/20240622_215528.jpg", "gneiss-hill/20240622_220432.jpg", "gneiss-hill/20240622_215525.jpg", "gneiss-hill/20240622_220439.jpg", "gneiss-hill/20240622_215454.jpg", "gneiss-hill/20240622_215551.jpg", "gneiss-hill/20240622_220449.jpg", "gneiss-hill/20240622_220458.jpg"],
                   "6": ["basecamp/Messenger_creation_896d3ff6-3681-4fc2-a273-3d94d29b1109.jpeg", "basecamp/Messenger_creation_e676ba9d-e9d6-4d1b-9f44-345e5dcbae52.jpeg", "basecamp/Messenger_creation_bf6b566f-89cd-4f54-b984-5961824303f8.jpeg"]
                 }

map_id_to_folder_name = {
    "1": "grotto",
    "2": "uog",
    "3": "grr",
    "4": "gneiss-banks",
    "5": "gneiss-hill",
    "6": "basecamp"
}

gym_routes = {
    "1": [
        {
            "id": 1,
            "climb_name": "Speedy Ascent",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V5",
            "climb_type": "slab",
            "hold_type": "crimps",
            "description": "Fast ascent on technical slab with small holds."
        },
        {
            "id": 2,
            "climb_name": "Echoing Heights",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "High-reaching climb on echoing overhang with pinch grips."
        },
        {
            "id": 3,
            "climb_name": "Dynamic Rush",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V6",
            "climb_type": "dynamic",
            "hold_type": "slopers",
            "description": "Energetic climb with dynamic moves on sloping holds."
        },
        {
            "id": 4,
            "climb_name": "Guelph Granite",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V4",
            "climb_type": "slab",
            "hold_type": "jugs",
            "description": "Smooth ascent on Guelph's distinctive granite with large jug holds."
        },
        {
            "id": 5,
            "climb_name": "Toppling Heights",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V3",
            "climb_type": "overhang",
            "hold_type": "pockets",
            "description": "Challenging climb on steep terrain with pocket holds."
        },
        {
            "id": 6,
            "climb_name": "Urban Traverse",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V8",
            "climb_type": "slab",
            "hold_type": "volumes",
            "description": "Traverse through city-inspired volumes on technical slab."
        },
        {
            "id": 7,
            "climb_name": "Downtown Dyno",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V10",
            "climb_type": "dynamic",
            "hold_type": "crimps",
            "description": "Dynamic ascent through downtown-themed crimps."
        },
        {
            "id": 8,
            "climb_name": "Grotto Grandeur",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V9",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "Grand overhang ascent with pinches at The Guelph Grotto."
        },
        {
            "id": 9,
            "climb_name": "Riverside Rhythm",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V11",
            "climb_type": "slab",
            "hold_type": "slopers",
            "description": "Flowing slab climb with rhythmic sloping holds."
        },
        {
            "id": 10,
            "climb_name": "Arboretum Ascent",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V12",
            "climb_type": "overhang",
            "hold_type": "jugs",
            "description": "Elevated climb amidst arboreal overhang with large jug holds."
        },
        {
            "id": 11,
            "climb_name": "Stone Arch",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V13",
            "climb_type": "dynamic",
            "hold_type": "pockets",
            "description": "Arch-shaped dynamic climb with challenging pocket holds."
        },
        {
            "id": 12,
            "climb_name": "Royal City Ridge",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V14",
            "climb_type": "slab",
            "hold_type": "volumes",
            "description": "Regal ascent along ridge-themed volumes on slab."
        },
        {
            "id": 13,
            "climb_name": "Speed River Summit",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V6",
            "climb_type": "slab",
            "hold_type": "crimps",
            "description": "Swift ascent with small crimps along Speed River."
        },
        {
            "id": 14,
            "climb_name": "Willow Whippers",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V8",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "Challenging ascent with whipper pinches on overhang."
        },
        {
            "id": 15,
            "climb_name": "Stonewall Step",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V7",
            "climb_type": "dynamic",
            "hold_type": "slopers",
            "description": "Dynamic climb with strategic steps on stonewall slopers."
        },
        {
            "id": 16,
            "climb_name": "Guelph Gravel",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V5",
            "climb_type": "slab",
            "hold_type": "jugs",
            "description": "Smooth ascent on gravel-themed slab with large jug holds."
        },
        {
            "id": 17,
            "climb_name": "Riverside Rapids",
            "gym_name": "The Guelph Grotto",
            "gym_id": "1",
            "v_rating": "V4",
            "climb_type": "overhang",
            "hold_type": "pockets",
            "description": "Rapid ascent through challenging pockets along riverside."
        }
    ],
    "2": [],
    "3": [
        {
            "id": 1,
            "climb_name": "Waterloo Summit",
            "gym_name": "Grand River Rocks",
            "gym_id": "3",
            "v_rating": "V6",
            "climb_type": "slab",
            "hold_type": "crimps",
            "description": "Reach the summit on technical slab with small crimps."
        },
        {
            "id": 2,
            "climb_name": "Laurier Ledge",
            "gym_name": "Grand River Rocks",
            "gym_id": "3",
            "v_rating": "V8",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "Navigate the ledge with challenging pinches on overhang."
        }
    ],
    "4": [
        {
            "id": 1,
            "climb_name": "Coastal Granite",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V5",
            "climb_type": "slab",
            "hold_type": "crimps",
            "description": "Technical slab route on coastal granite."
        },
        {
            "id": 2,
            "climb_name": "Whistler Peak",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "Challenging overhang resembling Whistler Peak."
        },
        {
            "id": 3,
            "climb_name": "Pacific Crest",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V6",
            "climb_type": "dynamic",
            "hold_type": "slopers",
            "description": "Dynamic route along the Pacific Crest."
        },
        {
            "id": 4,
            "climb_name": "Fraser River Gorge",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V4",
            "climb_type": "slab",
            "hold_type": "jugs",
            "description": "Scenic climb in the Fraser River Gorge area."
        },
        {
            "id": 5,
            "climb_name": "Vancouver Island",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V3",
            "climb_type": "overhang",
            "hold_type": "pockets",
            "description": "Exciting climb on Vancouver Island's rocky terrain."
        },
        {
            "id": 6,
            "climb_name": "Squamish Chief",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V8",
            "climb_type": "slab",
            "hold_type": "volumes",
            "description": "Challenging slab climb like the Squamish Chief."
        },
        {
            "id": 7,
            "climb_name": "Rocky Mountain High",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V10",
            "climb_type": "dynamic",
            "hold_type": "crimps",
            "description": "Elevated dynamic route in the Rockies."
        },
        {
            "id": 8,
            "climb_name": "Selkirk Alpine",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V9",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "Alpine overhang reminiscent of the Selkirk Mountains."
        },
        {
            "id": 9,
            "climb_name": "Canadian Shield",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V11",
            "climb_type": "slab",
            "hold_type": "slopers",
            "description": "Technical slab climb resembling the Canadian Shield."
        },
        {
            "id": 10,
            "climb_name": "Kootenay River",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V12",
            "climb_type": "overhang",
            "hold_type": "jugs",
            "description": "Flowing overhang inspired by the Kootenay River."
        },
        {
            "id": 11,
            "climb_name": "Bugaboos Alpine",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V13",
            "climb_type": "dynamic",
            "hold_type": "pockets",
            "description": "Dynamic pockets in an alpine setting like the Bugaboos."
        },
        {
            "id": 12,
            "climb_name": "Okanagan Valley",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V14",
            "climb_type": "slab",
            "hold_type": "volumes",
            "description": "Balanced movements on volume holds from the Okanagan Valley."
        },
        {
            "id": 13,
            "climb_name": "Cascade Range",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V6",
            "climb_type": "slab",
            "hold_type": "crimps",
            "description": "Technical slab climb in the Cascade Range."
        },
        {
            "id": 14,
            "climb_name": "Golden Ears Summit",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V8",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "Overhanging route with a summit view like Golden Ears."
        },
        {
            "id": 15,
            "climb_name": "Icefields Parkway",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V7",
            "climb_type": "dynamic",
            "hold_type": "slopers",
            "description": "Dynamic route along the Icefields Parkway."
        },
        {
            "id": 16,
            "climb_name": "Castle Crags",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V5",
            "climb_type": "slab",
            "hold_type": "jugs",
            "description": "Easy climb with large jug holds at Castle Crags."
        },
        {
            "id": 17,
            "climb_name": "Mount Robson",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V4",
            "climb_type": "overhang",
            "hold_type": "pockets",
            "description": "Challenging pockets inspired by Mount Robson."
        },
        {
            "id": 18,
            "climb_name": "Fraser River Canyon",
            "gym_name": "Gneiss Climbing - OG Banks",
            "gym_id": "4",
            "v_rating": "V9",
            "climb_type": "slab",
            "hold_type": "volumes",
            "description": "Delicate movements on volume holds in Fraser River Canyon."
        }
    ],
    "5": [
        {
            "id": 1,
            "climb_name": "Zenith",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V5",
            "climb_type": "slab",
            "hold_type": "crimps",
            "description": "Technical climb with small holds."
        },
        {
            "id": 2,
            "climb_name": "Gravity",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "Powerful overhanging route with pinch grips."
        },
        {
            "id": 3,
            "climb_name": "Serenity",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V6",
            "climb_type": "dynamic",
            "hold_type": "slopers",
            "description": "Dynamic moves on sloping holds."
        },
        {
            "id": 4,
            "climb_name": "Echo",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V4",
            "climb_type": "slab",
            "hold_type": "jugs",
            "description": "Easy climb with large jug holds."
        },
        {
            "id": 5,
            "climb_name": "Apex",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V3",
            "climb_type": "overhang",
            "hold_type": "pockets",
            "description": "Challenging pockets on steep terrain."
        },
        {
            "id": 6,
            "climb_name": "Breeze",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V8",
            "climb_type": "slab",
            "hold_type": "volumes",
            "description": "Delicate movements on volume holds."
        },
        {
            "id": 7,
            "climb_name": "Zephyr",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V10",
            "climb_type": "dynamic",
            "hold_type": "crimps",
            "description": "Powerful and dynamic crimp route."
        },
        {
            "id": 8,
            "climb_name": "Pinnacle",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V9",
            "climb_type": "overhang",
            "hold_type": "pinches",
            "description": "High-intensity pinch route."
        },
        {
            "id": 9,
            "climb_name": "Crest",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V11",
            "climb_type": "slab",
            "hold_type": "slopers",
            "description": "Technical slab with sloping holds."
        },
        {
            "id": 10,
            "climb_name": "Summit",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V12",
            "climb_type": "overhang",
            "hold_type": "jugs",
            "description": "Strenuous overhang with large jug holds."
        },
        {
            "id": 11,
            "climb_name": "Cascade",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V13",
            "climb_type": "dynamic",
            "hold_type": "pockets",
            "description": "Dynamic moves on pocket holds."
        },
        {
            "id": 12,
            "climb_name": "Ridge",
            "gym_name": "Gneiss Climbing - Hill Security",
            "gym_id": "5",
            "v_rating": "V14",
            "climb_type": "slab",
            "hold_type": "volumes",
            "description": "Balanced movements on volume holds."
        }
    ],
    "6": [
        {
            "id": 1,
            "climb_name": "Cityscape Crux",
            "gym_name": "Basecamp Climbing - Toronto",
            "gym_id": "6",
            "v_rating": "V6",
            "climb_type": "overhang",
            "hold_type": "slopers",
            "description": "Navigate the cityscape crux on sloping overhang holds."
        },
        {
            "id": 2,
            "climb_name": "Lakefront Ledge",
            "gym_name": "Basecamp Climbing - Toronto",
            "gym_id": "6",
            "v_rating": "V8",
            "climb_type": "slab",
            "hold_type": "jugs",
            "description": "Ascend to the lakefront ledge on easy slab with large jug holds."
        },
        {
            "id": 3,
            "climb_name": "Rooftop Dyno",
            "gym_name": "Basecamp Climbing - Toronto",
            "gym_id": "6",
            "v_rating": "V9",
            "climb_type": "dynamic",
            "hold_type": "pockets",
            "description": "Dynamic moves to the rooftop dyno with challenging pocket holds."
        }
    ]
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
    "4": {
        "id": 4,
        "gym_name": "Gneiss Climbing - OG Banks",
        "logo_image_url": "https://littlebuildingsolutions.com/wp-content/uploads/testimonial-image-gneissclimbing.png",
        "lat": 49.88472564990776,
        "lng": -119.42279193470492,
    },
    "5": {
        "id": 5,
        "gym_name": "Gneiss Climbing - Hill Security",
        "logo_image_url": "https://littlebuildingsolutions.com/wp-content/uploads/testimonial-image-gneissclimbing.png",
        "lat": 49.896709226472915,
        "lng": -119.48772919235698,
    },
    "6": {
        "id": 6,
        "gym_name": "Basecamp Climbing - Toronto",
        "logo_image_url": "https://mma.prnewswire.com/media/1097214/Basecamp_Climbing_Basecamp_Climbing_Opens_Second_Location_in_Tor.jpg?w=200",
        "lat": 43.64996207530534, 
        "lng": -79.39762343317936,
    }
}

def upload_image(binary_image_data, gcs_image_name):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to your service account key file relative to the current directory
    keyfile_path = os.path.join(current_directory, '..', '..', 'resources', 'gdschackathon2024-422307-aaca36ebdcaa.json')

    credentials = service_account.Credentials.from_service_account_file(
        keyfile_path)
    storage_client = storage.Client(credentials=credentials)

    bucket_name = 'route_images'
    bucket = storage_client.bucket(bucket_name)

    # Create a new blob and upload the file's content
    blob = bucket.blob(gcs_image_name)
    blob.upload_from_string(binary_image_data, content_type='image/png')

    print(f'File {binary_image_data} uploaded to {bucket_name} as {gcs_image_name}')

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
    print(gym)

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
        # print(result)
        return result

    # print(gym_routes)
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

    # print(gyms_info)
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
    image_data = data.get('image_data')
    image_name = data.get('image_name')

    # Do something about the photo
    _, base64_data = image_data.split(',')

    # Decode the base64-encoded image data to obtain the binary image data
    binary_image_data = base64.b64decode(base64_data)

    # Upload the photo to GCS Bucket
    upload_image(binary_image_data, map_id_to_folder_name[gym_id] + "/" + image_name)

    # construct new json object - climb_info 
    random_id = random.randint(1000, 5000)
    climb_info = {
        "id": random_id,
        "climb_name": climb_name,
        "gym_name": gym_name,
        "gym_id": gym_id,
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

    # print(gym_routes)
    return "Success", 200
