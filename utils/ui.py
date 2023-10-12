from colorama import init, Fore, Style

init()

def banner():
    print(Fore.GREEN + '-----------------------------------' + Style.RESET_ALL)
    print(Style.BRIGHT + '---- Barista Invoicing Tool v2 ----' + Style.RESET_ALL)
    print(Fore.GREEN + '-----------------------------------' + Style.RESET_ALL)
    print('''
    Welcome to the Barista Invoicing Tool v2. This is a Command Line Interface (CLI) tool designed to streamline
    the invoice process at the barista station.
    
    The tool works by integrating data from two primary sources:
    1. The dispensings report from the Schaerer portal.
    2. The Manual consumption report for the Barista Pros.
    
    QUICK START GUIDE:
    1. Ensure you have the latest Pret and L'or dashboards downloaded and placed in the 'data/input' folder.
    2. Export any data from the Schaerer portal and place it into the 'data/input' folder.
    3. Follow the prompts provided by the tool.
    
    If you encounter any issues while using this tool, please contact Matt Gibbons.''')
    print('\n')