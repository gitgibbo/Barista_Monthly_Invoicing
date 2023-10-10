import os
import pandas as pd
from utils.data_loading import load_data
from utils.data_processing import process_data, finalize_data
from utils.config import load_configuration
from utils.query import period_select, customer_select
from utils.distributor_select import distributor_selection
from utils.duplicate_remover import remove_duplicates_based_on_serial

def automator(directory_path):
    
    # create empty table list
    df_list = []


    # user selects the period they are invoicing
    period = period_select()

    # distributor select
    distributor = distributor_selection()

    # user informaion

    # Loop through each file in the directory
    for filename in os.listdir(directory_path):

        temp_dist = distributor

        # infer root filepath
        file_path = os.path.join(directory_path,filename)

        # preliminary loading of data, return the dataframe and the mode (SOUL or PRO)
        print(f'Loading file {filename}...')
        df, mode = load_data(file_path)

        # CORRECTION due to incorrect distributor name being used in the manual consumption files        
        if mode == 'PRO' and temp_dist == 'Expresso Plus':
            temp_dist = 'ESPRESSO PLUS'

        # Pass over data and bring both pro and soul data into alignment
        print(f'Cleaning {filename}...')
        cleaned = process_data(df, mode)

        # create final table taking into account configurations
        print(f'Processing {filename}...')
        table = finalize_data(cleaned, load_configuration(), temp_dist)

        # filters overal data by wht the user wants to process
        print(f'Filtering {filename} based on period: {period}, and {temp_dist} in {mode} mode.')
        #table = table[(table['Period'] == period) & (table['Customer'] == customer_select(table))]
        table = table[(table['Period'] == period) & (table['Customer'] == temp_dist)]

        #add table to list, ready to be joined
        print('Adding table....')
        df_list.append(table)
    
    # join the tables up
    print('Joining tables...')
    joined_table = pd.concat(df_list, ignore_index=True)

    final_table = remove_duplicates_based_on_serial(joined_table)

    # final sort
    print('Sorting table...')
    final_table = final_table.sort_values(by='Invoice Amount', ascending=False).reset_index(drop=True)


    return final_table, distributor
