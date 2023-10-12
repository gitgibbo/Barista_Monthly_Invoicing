# Barista Monthly Invoicing (BMI) Tool

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
    - [Modules and Functions](#modules-and-functions)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Known Issues](#known-issues)
8. [Support and Contributions](#support-and-contributions)
9. [License](#license)

## Overview

The Barista Monthly Invoicing (BMI) Tool is a Command-Line Interface (CLI) application designed to automate the invoicing process for automated barista machines. The tool simplifies data input, performs necessary calculations, and generates relevant invoicing information.

## Features

### Core Functionalities

- **Automates the Invoicing Process**: Streamlines data handling and calculations for coffee machine vends.
- **User-Friendly CLI**: Provides a simple and intuitive interface for users.
- **Configurable Settings**: Allows for customization through a JSON configuration file.
- **Data Handling**: Uses Pandas DataFrames for data manipulation and processing.
- **Modular Design**: Functionality is segregated into various modules for easier management and updates.

### Modules and Functions

- **Data Loading**: The `load_data()` function reads CSV files and imports them into Pandas DataFrames.
- **Data Processing**: Several functions are used to process data:
    - `convert_to_datetime`: Converts date formats and adds year-month data.
    - `calculate_null_vends`: Computes null vends based on specific conditions.
    - `compress_and_rename`: Aggregates and renames data columns.
- **Duplicate Removal**: Utilizes `remove_duplicates_based_on_serial` to eliminate redundant data.
- **User Configuration**: Features like invoicing period and distributor selection are user-configurable.

## Requirements

- Python 3.x
- Pandas library
- Additional Python packages listed in `requirements.txt`

## Installation

### 1. Download the Application

Download the ZIP file and unzip it into your preferred directory.

### 2. Install Dependencies

Navigate to the directory containing the unzipped files. Open a terminal window and execute:

```bash
pip install -r requirements.txt
```

## Configuration

Edit the `config.json` file to specify any default settings or preferences.

## Usage

After installation and configuration, navigate to the application directory and run the following:

**For Windows:**

```bash
InvoiceTool.bat
```

**For Unix/Linux:**

```bash
python main.py
```

Upon execution, the `automator` function orchestrates the entire invoicing process, from data loading to finalization.

## Known Issues

- The batch file is named `InvoiceTool.bat`, which could be confusing. Consider renaming it to `BMITool.bat` for clarity.

## Support and Contributions

For any issues or contributions, refer to the `.gitignore` file for what to exclude when updating the codebase.

## License

This project is open-source. Feel free to use, modify, and distribute as you see fit.
