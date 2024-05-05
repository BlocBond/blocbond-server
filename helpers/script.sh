# Set the path to the input image file
input_image="test.png"

# Set the path to the output resized image file
output_image="resized_image.png"

# Use sips to resize the image to a 3:2 aspect ratio
# Replace "640" and "520" with your desired width and height
sips -z 520 640 "$input_image" --out "$output_image"