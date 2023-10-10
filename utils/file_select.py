import os

def file_select():
    # set variables
    folder_path = 'data/input'
    files = os.listdir(folder_path)

    # list files contained in the directory
    print('\nFiles in the "data/input" directory:\n')
    for i, file_name in enumerate(files):
        print(f'{i+1}. {file_name}')
    if not files:
        print('\nNo files found in the input folder.\n')
        return None
    
    # create selection function
    while True:
        choice = input('\nEnter the number of the file you would like to load: ')
        if not choice.isdigit():
            print('Invalid input. Please enter a valid number.')
            continue

        index = int(choice)-1
        if index < 0 or index >= len(files):
            print('Invalid input. Please enter a valid number.')
            continue

        file_path = os.path.join(folder_path, files[index])
        break
    return file_path