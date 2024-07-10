date_pattern = re.compile(r'^\d{8}$')

date_folders = [folder for folder in folders if date_pattern.search(folder.split('/')[-1])]

date_folders.sort()
