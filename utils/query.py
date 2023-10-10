import re
import pandas as pd

def period_select():
    period_string = input('Enter period being invoiced in MM/YYYY format: ')
    try:
        while not re.match(r"(\d{2})/(\d{4})", period_string):
            print('\nInvalid format. Please enter a date in the format MM/YYYY.\n')
            period_string = input('\nEnter period being invoiced in MM/YYYY format:\n')
    except ValueError:
        print('not good')

    match = re.match(r"(\d{2})/(\d{4})", period_string)

    filter_date = pd.Period(period_string, freq='M')

    return filter_date

def customer_select(table):
    customers = table['Customer'].unique()
    print('\nDistributor selection:\n')
    for i, customer in enumerate(customers):
        print(f'{i+1}. {customer}')
    print(f'{len(customers)+1}. No Selection')
    


    while True:
        choice = input('\nEnter the number of the Distributor you are processing: ')
        if not choice.isdigit():
            print('Invalid input. PLease enter a valid number.')
            continue

        index = int(choice)-1
        if index < 0 or index >= len(customers)+1:
            print('Invalid input. Please enter a valid number.')
            continue
        elif index == len(customers):
            distributor = 'NO SELECTION'
            break
        distributor = customers[index]
        break
    
    return distributor