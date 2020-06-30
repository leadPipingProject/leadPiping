# Instructions to This Repository

## How to reproduce the data

### Step 1: supply the raw data into raw-data folder

*Create a folder called `raw-data`, and put the following data files into the folder as they are*.

- `raw-data/SW - All Lead WQ Samples (2010-18).xls`
- `raw-data/SW - Comm pipe data.xls`
- `raw-data/SW - Lead Comm Pipe Replacements (2004-2018).csv`
- `raw-data/SW - Phosphate Dosing WTWs Y or N.xlsx`
- `raw-data/SW - Postcodes linked to SW Zonal Structure.xlsb`
- `raw-data/SW - Scottish Water Zonal Phosphate Levels.xls`
- `Other - Postcode_ household count_ urban class.csv`
- `Other - SAA_PropertyAgeData.csv`
- `Other - UK-HPI-full-file-2019-03.csv`

The file names must be **exactly** the same as listed above.
(Data files are not supplied with the repository because of file size limit imposed by github.)

### Step 2: set working directory (cd) to repository folder

Set the working directory of the notebooks/scripts to the
**repository root** (workspace folder), NOT the script folder.
(Otherwise, the scripts cannot find the data files).

The easiest way is to do this is to use linux/unix `cd` command:
`cd {path to this repository folder}` before running python.

### Step 3: run `python code-clean/clean_main.py`

Only need to run `python code-clean/clean_main.py`.
This script `clean_main.py` will automatically execute the other scripts.
