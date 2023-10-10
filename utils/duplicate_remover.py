import pandas as pd

def remove_duplicates_based_on_serial(dataframe):
    """
    Removes duplicate records from a DataFrame based on the 'serial' column.
    
    Parameters:
        dataframe (pd.DataFrame): The DataFrame containing the records.
        
    Returns:
        pd.DataFrame: A new DataFrame with duplicate records removed.
    """
    if dataframe is None or dataframe.empty:
        print("The DataFrame is empty or None. No operation performed.")
        return dataframe

    # Check if 'serial' column exists
    if 'Serial Number' not in dataframe.columns:
        print("The column 'serial' does not exist in the DataFrame. No operation performed.")
        return dataframe

    # Remove duplicates
    dataframe_deduplicated = dataframe.drop_duplicates(subset=['Serial Number'], keep='first')

    print(f"Removed {len(dataframe) - len(dataframe_deduplicated)} duplicate records based on 'serial' column.")
    
    return dataframe_deduplicated
