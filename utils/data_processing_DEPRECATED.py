import pandas as pd
import numpy as np

def process_data(data, mode):
    def process_soul(data):
        # convert date column to datetime
        data['LocalDate'] = pd.to_datetime(data['LocalDate'])
        # calculate 'YearMonth' column (for grouping)
        data['YearMonth'] = data['LocalDate'].dt.to_period('M')
        # group table
        grouped_data = data.groupby(['HierarchyPath', 'MachineNumber', 'MachineName', 'YearMonth', 'RecipeName', 'Canceled']).size().reset_index(name='NumberOfDispensings')
        # calculate null vends
        grouped_data['Null Vends'] = np.where((grouped_data['RecipeName'] == 'Splash of milk [S]') | (grouped_data['Canceled'] == 'canceled'), grouped_data['NumberOfDispensings'], 0)
        # compress table
        compressed_data = grouped_data[['HierarchyPath', 'MachineNumber', 'MachineName', 'YearMonth', 'NumberOfDispensings', 'Null Vends']].groupby(['HierarchyPath', 'MachineNumber', 'MachineName', 'YearMonth'])[['NumberOfDispensings', 'Null Vends']].sum().reset_index()
        # sort out hierarchypath
        compressed_data['HierarchyPath'] = compressed_data['HierarchyPath'].str.replace(r'^UK/PRET/', '', regex=True)
        # rename columns
        compressed_data.rename(columns={'HierarchyPath':'Customer', 'MachineNumber':'Serial Number', 'MachineName':'Machine Name', 'YearMonth':'Period', 'NumberOfDispensings':'Actual Vends'}, inplace=True)
        return compressed_data
    def process_pro(data):
        # convert date colum  to datetime
        data['Date'] = pd.to_datetime(data['Date'])

        # calculate 'YearMonth' column (for grouping)
        data['YearMonth'] = data['Date'].dt.to_period('M')

        # drop all the uselss columns
        data = data[['serial_number', 'organization', 'Date', 'MonthInYear', 'WeekInYear', 'vends_delta', 'paid_vends_delta', 'free_vends_delta', 'customer', 'local_code_description', 'YearMonth']].reset_index(drop=True)

        # calcualte null vends
        data['Null Vends'] = np.where((data['local_code_description'] == 'SPLASH OF MILK') | (data['local_code_description'] == 'ESPRESSO SHOT') | (data['local_code_description'] == 'SYRUP SHOT'), data['vends_delta'], 0)

        # compress table
        compressed_data = data[['customer', 'serial_number', 'organization', 'YearMonth', 'vends_delta', 'Null Vends']].groupby(['customer','serial_number', 'organization', 'YearMonth'])[['vends_delta', 'Null Vends']].sum().reset_index()
        
        # sort out serial number
        compressed_data['serial_number'] = compressed_data['serial_number'].str.replace(r'^SAR', '', regex=True)
        # rename columns
        compressed_data.rename(columns={'customer':'Customer', 'serial_number':'Serial Number', 'organization':'Machine Name', 'YearMonth':'Period', 'vends_delta':'Actual Vends'}, inplace=True)

        return compressed_data
    if mode == 'SOUL':
       compressed_data = process_soul(data)

    elif mode == 'PRO':
        compressed_data = process_pro(data)

    else:
        return None

    # calculate null vends
    compressed_data['Valid Vends'] = compressed_data['Actual Vends'] - compressed_data['Null Vends']

    return compressed_data

def finalize_data(data, settings, distributor):
    # import settings
    wastage = settings['wastage_per_month']
    #cpd_bins = settings['cpd_bins']
    #hire_charges = settings['hire_charges']
    minimum_hire_charge = settings['minimum_hire_charge']
    #cpd_bins = settings['cpd_bins']

    if distributor == 'DC7':
        hire_charge_matrix = {
            (0, 15): 2.25,
            (15, 30): 1.26,
            (30, 50): 0.86,
            (50, 80): 0.62,
            (80, float('inf')): 0.55,
        }
    elif distributor == 'ESPRESSO PLUS' or 'Expresso Plus':
        hire_charge_matrix = {
            (0, 20): 1.26,
            (20, 25): 0.98,
            (25, 30): 0.90,
            (30, 40): 0.86,
            (40, 50): 0.75,
            (50, 60): 0.62,
            (60, 70): 0.60,
            (70, float('inf')): 0.58,
        }

    def get_hire_charge(num_vends):
        for key, value in hire_charge_matrix.items():
            lower, upper = key
            if lower <= num_vends/365 < upper:
                return value
        return "Invalid Number of Vends"



    # # New commericals function
    # def get_hire_charge_old(vends_per_year):
    #     if vends_per_year > cpd_bins[6] * 365:
    #         return hire_charges[7]
    #     if vends_per_year > cpd_bins[5] * 365:
    #         return hire_charges[6]
    #     if vends_per_year > cpd_bins[4] * 365:
    #         return hire_charges[5]
    #     if vends_per_year > cpd_bins[3] * 365:
    #         return hire_charges[4]
    #     if vends_per_year > cpd_bins[2] * 365:
    #         return hire_charges[3]
    #     if vends_per_year > cpd_bins[1] * 365:
    #         return hire_charges[2]
    #     if vends_per_year > cpd_bins[0] * 365:
    #         return hire_charges[1]
    #     if vends_per_year >= 0:
    #         return hire_charges[0]
        
    # add wastage parameter to monthly records
    data['Wastage'] = wastage

    # true throughput calculation
    data['True Throughput'] = (data['Valid Vends'] - data['Wastage']).clip(lower=0)

    # Annualised Calculation
    data['Days in Month'] = data['Period'].apply(lambda x: x.days_in_month)
    data['Annualised Throughput'] = ((data['True Throughput'] / data['Days in Month']) * 365).astype(int)

    # Select Hire charge using function above
    #data['Hire Charge'] = data['Annualised Throughput'].apply(get_hire_charge).clip(lower=minimum_hire_charge)
    data['Hire Charge'] = data['Annualised Throughput'].apply(get_hire_charge).clip(lower=minimum_hire_charge)

    # Calculate invoice amount
    data['Invoice Amount'] = data['True Throughput'] * data['Hire Charge']
    return data