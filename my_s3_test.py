import os
import base64

def decode_file(enc_file_path, txt_file_path):
    with open(enc_file_path, 'rb') as enc_file:
        encoded_data = enc_file.read()
    
    decoded_data = base64.b64decode(encoded_data)
    
    with open(txt_file_path, 'wb') as txt_file:
        txt_file.write(decoded_data)

def convert_enc_to_txt_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.enc'):
            enc_file_path = os.path.join(folder_path, filename)
            txt_file_path = os.path.splitext(enc_file_path)[0] + '.txt'
            decode_file(enc_file_path, txt_file_path)
            print(f'Converted {enc_file_path} to {txt_file_path}')

folder_path = 'test_folders'
convert_enc_to_txt_in_folder(folder_path)
