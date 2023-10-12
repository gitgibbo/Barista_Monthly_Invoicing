# Import necessary modules and functions
from utils.automate import automator
from utils.cmds import clear_terminal
from utils.ui import banner
from utils.save import save_dataframe
import pandas as pd
from utils.config import load_configuration
import math

# Load configuration settings from a file. This typically includes paths and other variables.
config = load_configuration()

# Main loop to keep the tool running until the user decides to exit
while True:
    # Clear the terminal for a clean view
    clear_terminal()
    
    # Display a banner or header for the tool
    banner()

    # Try to automate the data collection and processing
    try:
        data, distributor = automator(config['input_directory'])
    except FileNotFoundError as e:  # File not found error
        print(f"File not found: {e}")
        exit(1)
    except Exception as e:  # Any other exception
        print(f"An unknown error occurred: {e}")
        exit(1)

    # Check if any data was processed
    if data.empty:
        print("No data to process. Exiting.")
        exit(1)

    # Calculate the total invoice amount and round it down to two decimal places
    total_invoice_amount = data["Invoice Amount"].sum()
    rounded_total_invoice_amount = math.floor(total_invoice_amount * 100) / 100
    print(f'\nThe total invoice amount for this period is £{rounded_total_invoice_amount}\n')

    # Save the processed data to a file
    print('Saving Data!')
    print(save_dataframe(data, directory_path=config['output_directory'], custom_name=f'{distributor}_{data.iloc[0, 3]}'.lower()))

    # Ask the user if they want to restart the tool
    restart = input('Do you want to restart the tool? (y/n): ')

    # Exit the tool if the user enters anything other than 'y'
    if restart.lower() != 'y':
        clear_terminal()  # Clear terminal before exiting
        break
