# import tools
import pandas as pd

def load_data(file_path):
    if file_path.endswith('.csv'):
        try:
            df = pd.read_csv(file_path)
            mode = 'SOUL'
        except pd.errors.ParserError:
            print('The selected file is not a valid csv file.')
    elif file_path.endswith('.xlsx'):
        try:
            df = pd.read_excel(file_path, sheet_name = 'flatten view')
            mode = 'PRO'
        except pd.errors.ParserError:
            print('File is not a valid excel file.')
    else: return None
    return df, mode
