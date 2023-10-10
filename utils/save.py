import pandas as pd
import os
from datetime import datetime

def save_dataframe(df, directory_path='./data/output', file_format='csv', custom_name=None, datestamp=True):
    """
    Save a Pandas DataFrame to a file.

    Parameters:
        df (DataFrame): The DataFrame to save.
        directory_path (str): The directory where to save the file. Defaults to the current directory.
        file_format (str): The file format to use ('csv' or 'excel'). Defaults to 'csv'.
        custom_name (str): Custom name for the file. Defaults to None.
        datestamp (bool): Whether to prefix the filename with a date stamp. Defaults to True.

    Returns:
        str: The path of the saved file.
    """
    
    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    # Generate date stamp
    date_prefix = ''
    if datestamp:
        date_prefix = datetime.now().strftime('%Y%m%d_')
    
    # Generate file name
    if custom_name:
        filename = f"{date_prefix}{custom_name}"
    else:
        filename = f"{date_prefix}dataframe"
    
    # Generate full file path
    if file_format == 'csv':
        file_path = os.path.join(directory_path, f"{filename}.csv")
        df.to_csv(file_path, index=False)
    elif file_format == 'excel':
        file_path = os.path.join(directory_path, f"{filename}.xlsx")
        df.to_excel(file_path, index=False)
    else:
        raise ValueError("Invalid file format. Choose either 'csv' or 'excel'.")
    
    return f"DataFrame saved to: {file_path}"

# Example usage:
# df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
# save_dataframe(df, directory_path='./output', file_format='csv', custom_name='my_data')
