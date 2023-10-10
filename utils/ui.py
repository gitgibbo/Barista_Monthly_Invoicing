from colorama import init, Fore, Style

init()

def banner():
    print(Fore.GREEN + '-----------------------------------' + Style.RESET_ALL)
    print(Style.BRIGHT + '---- Barista Invoicing Tool v2 ----' + Style.RESET_ALL)
    print(Fore.GREEN + '-----------------------------------' + Style.RESET_ALL)
    print('''
    This is a CLI tool designed to facilitate the barista station invoice process.
    it works by taking in the two primary sources of data, the dispensings report from the schaerer portal,
    and the Manual consumption report for the barista pros.
          
    QUICK START INSTRUCTIONS:
          1. Make sure you have the latest pret and L'or dashboards downloaded and in the data/input folder.
          2. Put any data exports from the schaerer portal into the data/input folder
          3. follow the prompts below!
          
    If you have any problems using this tool, please notify Matt Gibbons.''')
    print('\n')