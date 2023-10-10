def distributor_selection():
    distributors = {
        1:'Expresso Plus',
        2:'DC7'}
    print('Please select a distributor:')
    for key, value in distributors.items():
        print(f'{key}. {value}')
    
    while True:
        choice = input('\nEnter the number of the distributor: ')
        if not choice.isdigit():
            print('Invalid input. Please enter a valid number.')
            continue
        index = int(choice)-1
        if index < 0 or index >= len(distributors):
            print('Invalid input. Please enter a valid number.')
            continue
        print(list(distributors.items())[index][1])
        result = list(distributors.items())[index][1]
        break
    return result