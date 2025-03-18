import os

five = open('flag-1(5).jpg', 'rb').read()
def list_files(directory):
    try:
        files = sorted(os.listdir(directory))  # Sort files for better readability
        for file in files:
            k = open(file, 'rb').read()
            res = five + k
            open('./files/{}'.format(file), 'wb').write(res)
            print('success {i}')
    except FileNotFoundError:
        print("Directory not found.")

list_files("./")
