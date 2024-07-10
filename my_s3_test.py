date_pattern = re.compile(r'^\d{8}$')

date_folders = [folder for folder in folders if date_pattern.search(folder.split('/')[-1])]

date_folders.sort()

# Check if there are more than 3 folders
if len(date_folders) > 3:
    # Get the folders to delete, which are all except the latest 3
    folders_to_delete = date_folders[:-3]

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
