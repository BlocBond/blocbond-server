from google.cloud import storage

# Initialize a client
storage_client = storage.Client()

bucket_name = 'route_images'

# Specify the name of the file to upload
source_file_name = 'images/BlocBondLogo.png'

# Specify the destination object name
destination_blob_name = 'BlocBondLogo.png'

# Get the bucket
bucket = storage_client.bucket(bucket_name)

# Create a new blob and upload the file's content
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)

print(f'File {source_file_name} uploaded to {bucket_name} as {destination_blob_name}')
