import pandas as pd
import numpy as np

def convert_to_datetime(data, column_name, new_column_name):
    data[new_column_name] = pd.to_datetime(data[column_name])
    data['YearMonth'] = data[new_column_name].dt.to_period('M')

def calculate_null_vends(data, conditions, column_name, new_column_name):
    data[new_column_name] = np.where(conditions, data[column_name], 0)

def compress_and_rename(data, group_columns, sum_columns, rename_dict):
    compressed_data = data[group_columns + sum_columns].groupby(group_columns)[sum_columns].sum().reset_index()
    compressed_data.rename(columns=rename_dict, inplace=True)
    return compressed_data

def process_data(data, mode):
    if mode == 'SOUL':
        convert_to_datetime(data, 'LocalDate', 'LocalDate')
        grouped_data = data.groupby(['HierarchyPath', 'MachineNumber', 'MachineName', 'YearMonth', 'RecipeName', 'Canceled']).size().reset_index(name='NumberOfDispensings')
        calculate_null_vends(grouped_data, (grouped_data['RecipeName'] == 'Splash of milk [S]') | (grouped_data['Canceled'] == 'canceled'), 'NumberOfDispensings', 'Null Vends')
        compressed_data = compress_and_rename(
            grouped_data,
            ['HierarchyPath', 'MachineNumber', 'MachineName', 'YearMonth'],
            ['NumberOfDispensings', 'Null Vends'],
            {'HierarchyPath': 'Customer', 'MachineNumber': 'Serial Number', 'MachineName': 'Machine Name', 'YearMonth': 'Period', 'NumberOfDispensings': 'Actual Vends'}
        )
        compressed_data['Customer'] = compressed_data['Customer'].str.replace(r'^UK/PRET/', '', regex=True)


    elif mode == 'PRO':
        convert_to_datetime(data, 'Date', 'Date')
        calculate_null_vends(data, (data['local_code_description'].isin(['SPLASH OF MILK', 'ESPRESSO SHOT', 'SYRUP SHOT'])), 'vends_delta', 'Null Vends')
        compressed_data = compress_and_rename(
            data,
            ['customer', 'serial_number', 'organization', 'YearMonth'],
            ['vends_delta', 'Null Vends'],
            {'customer': 'Customer', 'serial_number': 'Serial Number', 'organization': 'Machine Name', 'YearMonth': 'Period', 'vends_delta': 'Actual Vends'}
        )
        compressed_data['Serial Number'] = compressed_data['Serial Number'].str.replace(r'^SAR', '', regex=True)
    else:
        return None

    compressed_data['Valid Vends'] = compressed_data['Actual Vends'] - compressed_data['Null Vends']
    return compressed_data

def finalize_data(data, settings, distributor):
    wastage = settings['wastage_per_month']
    minimum_hire_charge = settings['minimum_hire_charge']
    hire_charge_matrix = get_hire_charge_matrix(distributor)
    
    data['Wastage'] = wastage
    data['True Throughput'] = (data['Valid Vends'] - data['Wastage']).clip(lower=0)
    data['Days in Month'] = data['Period'].apply(lambda x: x.days_in_month)
    data['Annualised Throughput'] = ((data['True Throughput'] / data['Days in Month']) * 365).astype(int)
    data['Hire Charge'] = data['Annualised Throughput'].apply(lambda x: get_hire_charge(x, hire_charge_matrix)).clip(lower=minimum_hire_charge)
    data['Invoice Amount'] = data['True Throughput'] * data['Hire Charge']
    return data

def get_hire_charge_matrix(distributor):
    if distributor == 'DC7':
        return {
            (0, 15): 2.25,
            (15, 30): 1.26,
            (30, 50): 0.86,
            (50, 80): 0.62,
            (80, float('inf')): 0.55,
        }
    elif distributor in ['ESPRESSO PLUS', 'Expresso Plus']:
        return {
            (0, 20): 1.26,
            (20, 25): 0.98,
            (25, 30): 0.90,
            (30, 40): 0.86,
            (40, 50): 0.75,
            (50, 60): 0.62,
            (60, 70): 0.60,
            (70, float('inf')): 0.58,
        }

def get_hire_charge(num_vends, hire_charge_matrix):
    for key, value in hire_charge_matrix.items():
        lower, upper = key
        if lower <= num_vends / 365 < upper:
            return value
    return "Invalid Number of Vends"
