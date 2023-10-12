import pandas as pd
import numpy as np
from config import DC7_HIRE_CHARGE_MATRIX, EXPRESSO_PLUS_HIRE_CHARGE_MATRIX, EP_minimum_hire_charge, DC7_minimum_hire_charge, wastage_per_month

def convert_to_datetime(data, column_name):
    try:
        data[column_name] = pd.to_datetime(data[column_name])
    except:
        data[column_name] = pd.to_datetime(data[column_name], dayfirst=True)
        
    data['YearMonth'] = data[column_name].dt.to_period('M')

def calculate_null_vends(data, conditions, column_name, new_column_name):
    data[new_column_name] = np.where(conditions, data[column_name], 0)

def compress_and_rename(data, group_columns, sum_columns, rename_dict):
    compressed_data = data[group_columns + sum_columns].groupby(group_columns)[sum_columns].sum().reset_index()
    compressed_data.rename(columns=rename_dict, inplace=True)
    return compressed_data

def process_soul_data(data):
    # Convert the 'LocalDate' column to datetime format
    convert_to_datetime(data, 'LocalDate')
    
    # Group the data by the specified columns and calculate the size of each group
    grouped_data = data.groupby(['HierarchyPath', 'MachineNumber', 'MachineName', 'YearMonth', 'RecipeName', 'Canceled']).size().reset_index(name='NumberOfDispensings')
    
    # Calculate the null vends based on the specified conditions
    calculate_null_vends(grouped_data, (grouped_data['RecipeName'] == 'Splash of milk [S]') | (grouped_data['Canceled'] == 'canceled'), 'NumberOfDispensings', 'Null Vends')
    
    # Compress and rename the columns of the grouped data
    compressed_data = compress_and_rename(
        grouped_data,
        ['HierarchyPath', 'MachineNumber', 'MachineName', 'YearMonth'],
        ['NumberOfDispensings', 'Null Vends'],
        {'HierarchyPath': 'Customer', 'MachineNumber': 'Serial Number', 'MachineName': 'Machine Name', 'YearMonth': 'Period', 'NumberOfDispensings': 'Actual Vends'}
    )
    
    # Remove the prefix 'UK/PRET/' from the 'Customer' column
    compressed_data['Customer'] = compressed_data['Customer'].str.replace(r'^UK/PRET/', '', regex=True)
    
    # Calculate the valid vends by subtracting the null vends from the actual vends
    compressed_data['Valid Vends'] = compressed_data['Actual Vends'] - compressed_data['Null Vends']
    
    return compressed_data

def process_pro_data(data):
    convert_to_datetime(data, 'Date')
    calculate_null_vends(data, (data['local_code_description'].isin(['SPLASH OF MILK', 'ESPRESSO SHOT', 'SYRUP SHOT'])), 'vends_delta', 'Null Vends')
    compressed_data = compress_and_rename(
        data,
        ['customer', 'serial_number', 'organization', 'YearMonth'],
        ['vends_delta', 'Null Vends'],
        {'customer': 'Customer', 'serial_number': 'Serial Number', 'organization': 'Machine Name', 'YearMonth': 'Period', 'vends_delta': 'Actual Vends'}
    )
    compressed_data['Serial Number'] = compressed_data['Serial Number'].str.replace(r'^SAR', '', regex=True)
    compressed_data['Valid Vends'] = compressed_data['Actual Vends'] - compressed_data['Null Vends']
    return compressed_data

def process_data(data, mode):
    if mode == 'SOUL':
        return process_soul_data(data)
    elif mode == 'PRO':
        return process_pro_data(data)
    else:
        return None

def finalize_data(data, distributor):
    hire_charge_matrix, minimum_hire_charge = get_hire_charge_matrix(distributor)
    data['Wastage'] = wastage_per_month
    data['True Throughput'] = (data['Valid Vends'] - data['Wastage']).clip(lower=0)
    data['Days in Month'] = data['Period'].apply(lambda x: x.days_in_month)
    data['Annualised Throughput'] = ((data['True Throughput'] / data['Days in Month']) * 365).astype(int)
    data['Hire Charge'] = data['Annualised Throughput'].apply(lambda x: get_hire_charge(x, hire_charge_matrix))
    data['Invoice Amount'] = (data['True Throughput'] * data['Hire Charge']).clip(lower = minimum_hire_charge)
    return data

def get_hire_charge_matrix(distributor):
    if distributor == 'DC7':
        return DC7_HIRE_CHARGE_MATRIX, DC7_minimum_hire_charge
    elif distributor in ['ESPRESSO PLUS', 'Expresso Plus']:
        return EXPRESSO_PLUS_HIRE_CHARGE_MATRIX, EP_minimum_hire_charge
    
def get_hire_charge(num_vends, hire_charge_matrix):
    for key, value in hire_charge_matrix.items():
        lower, upper = key
        if lower <= num_vends / 365 < upper:
            return value
    return "Invalid Number of Vends"
