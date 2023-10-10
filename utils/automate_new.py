import os
import pandas as pd
from utils.data_loading import load_data
from utils.data_processing import process_data, finalize_data
from utils.config import load_configuration
from utils.query import period_select, customer_select
from utils.distributor_select import distributor_selection
from utils.duplicate_remover import remove_duplicates_based_on_serial

def automator(directory_path):
    try:
        # Initialize
        df_list = []
        period = period_select()
        distributor = distributor_selection()
        config = load_configuration()

        # Loop through each file in the directory
        for filename in os.listdir(directory_path):
            temp_distributor = distributor
            file_path = os.path.join(directory_path, filename)

            print(f'\nLoading file {filename}...')
            df, mode = load_data(file_path)

            # Correct distributor name if necessary
            if mode == 'PRO' and temp_distributor == 'Expresso Plus':
                temp_distributor = 'ESPRESSO PLUS'

            print(f'Processing...')
            cleaned_df = process_data(df, mode)
            processed_table = finalize_data(cleaned_df, config, temp_distributor)

            print(f'Filtering based on period: {period} and distributor: {temp_distributor} in {mode} mode.')
            filtered_table = processed_table[(processed_table['Period'] == period) & (processed_table['Customer'] == temp_distributor)]

            print('Adding table to list...')
            df_list.append(filtered_table)

        # Concatenate and deduplicate tables
        print('\nJoining tables...')
        joined_table = pd.concat(df_list, ignore_index=True)
        final_table = remove_duplicates_based_on_serial(joined_table)

        # Sort table by 'Invoice Amount'
        print('Sorting table...')
        final_table = final_table.sort_values(by='Invoice Amount', ascending=False).reset_index(drop=True)

        return final_table, distributor

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
