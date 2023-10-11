# Barista Invoicing Tool
# This script automates the invoicing process for coffee machine vends.
# It imports utility functions for automation, UI rendering, and data saving.

from utils.automate import automator
from utils.cmds import clear_terminal
from utils.ui import banner
from utils.save import save_dataframe
import pandas as pd
from utils.config import load_configuration
import math

# Load configuration settings
config = load_configuration()

# Set some display options
pd.set_option('display.max_rows', None)

while True:

    # Clear terminal
    clear_terminal()

    # Display banner
    banner()
    # Automate data collection and processing
    try:
        data, distributor = automator(config['input_directory'])
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    # Save the processed data
    if data.empty:
        print("No data to process. Exiting.")
        exit(1)

    total_invoice_amount = data["Invoice Amount"].sum()
    rounded_total_invoice_amount = math.floor(total_invoice_amount * 100) / 100
    print(f'\nThe total invoice amount for this period is £{rounded_total_invoice_amount}\n')

    print('Saving Data!')
    print(save_dataframe(data, directory_path= config['output_directory'], custom_name=f'{distributor}_{data.iloc[0, 3]}'.lower()))

    restart = input('Do you want to restart the tool? (y/n): ')

    if restart.lower != 'y':
        clear_terminal()
        break