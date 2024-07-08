import boto3

# Replace 'your_bucket_name' with your actual S3 bucket name
bucket_name = 'res-athena-access-test-bucket-april-2'
s3 = boto3.client('s3')

# List all objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')

# Extract the folder names
folders = [prefix['Prefix'].rstrip('/') for prefix in response.get('CommonPrefixes', [])]

# Sort the folders by date
folders.sort()

# Check if there are more than 3 folders
if len(folders) > 3:
    # Get the folders to delete, which are all except the latest 3
    folders_to_delete = folders[:-3]

    for folder in folders_to_delete:
        # List objects within the folder
        objects_to_delete = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'{folder}/')

        # Delete all objects within the folder
        delete_objects = [{'Key': obj['Key']} for obj in objects_to_delete.get('Contents', [])]
        if delete_objects:
            s3.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_objects})

        print(f"Deleted folder: {folder}")
else:
    print("No folder to delete. There are 3 or fewer folders.")
