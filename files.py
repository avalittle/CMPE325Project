import os

# Constants
SOUNDS_DIR = 'sounds/'

def save_file(filepath, file):
    print(filepath)
    file.save(SOUNDS_DIR + filepath)
    print("File uploaded successfully!")
    
def delete_file(filepath):
    os.remove(filepath)
    print("File successfully deleted!")
