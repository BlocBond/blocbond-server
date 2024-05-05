from src.app import app
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from google.cloud import storage

gym_routes = {
    "grotto": [
        {
            "id": 1,
            "climb_name": "Helicopter",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
        },
        {
            "id": 1,
            "climb_name": "Helicopter",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
        },
        {
            "id": 1,
            "climb_name": "Helicopter",
            "v_rating": "V7",
            "climb_type": "overhang",
            "hold_type": "crimps",
        },
    ]
}

def generate_signed_url(file_name_path):
    storage_client = storage.Client()

    bucket_name = 'route_images'
    bucket = storage_client.bucket(bucket_name)

    # Get a blob (file) from the bucket
    blob = bucket.blob(file_name_path)

    url = blob.generate_signed_url(expiration=7200) 
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
            route["climb_photo_url"] = image_url

    return gym_routes



    
