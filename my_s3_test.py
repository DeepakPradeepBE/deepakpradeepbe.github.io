def extract_timestamp(db_name):
    match = re.search(r'dev_gk_output_step(\d{8})_test', db_name)
    if match:
        try:
            # Check if the date is valid
            return datetime.strptime(match.group(1), '%Y%m%d')
        except ValueError:
            # Invalid date
            return None
    return None

def cleanup_older_glue_database():
    glue_client = session.client('glue')
    list_database = glue_client.get_databases()
    databases = list_database['DatabaseList']

    # Filter databases by the pattern and extract timestamp
    db_timestamps = [(db['Name'], extract_timestamp(db['Name'])) for db in databases]
    # Remove entries with no timestamp or invalid timestamp
    db_timestamps = [entry for entry in db_timestamps if entry[1] is not None]
    # Sort databases by timestamp in descending order
    db_timestamps.sort(key=lambda x: x[1], reverse=True)
    # Keep the latest 3 databases
    database_to_keep = db_timestamps[:3]
    # Set of database names to keep
    database_to_keep_set = {db[0] for db in database_to_keep}
    # Prepare databases to delete
    database_to_delete = [db_name for db_name, _ in db_timestamps if db_name not in database_to_keep_set]
    logger.info(f'Deleting the older Glue databases based on Timestamp {database_to_delete}')
    # Delete databases that are not in the keep_set
    for db_name in database_to_delete:
        logger.info(f'Deleting the Glue database {db_name}')
        glue_client.delete_database(Name=db_name)
