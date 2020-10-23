# Documentation

## Installation Instructions


- Clone the repository
- Install the environment with the commands
    `conda env create -f environment.yml`
- To activate the environment run 
    `conda activate DAAQS`
- Then go to the cfg.py file in DAAQS/utils
    - set the `cams_folder` path
    A typical cams_folder will contain files like "particulate_matter_2.5um_2019-01-24.nc"  
    - set the `openaq_folder` path
    A typical openaq_folder will contain files like "2019-01-01/1514765764.ndjson.gz"
- It is a good practice to create a plots folder in the main repository and save the plots there. plots is already added in gitignore.

## Files and functions

### io_cams.py

##### Description
- This file contains functions that are responsble for reading cams data.
- The file contains only one class called `CAMSData` and needs three argumets for initialisation.
    - `day` (str) : string date for which data is to be read
    - `span` (int) : number of days before and after the day for which the data is to be read
    - `parameter` (str) : parameter for which data is to be read. Example "pm25"
- Data can be accesed from `CAMSData` using `.data` object

- The returned `.data` object is a 3-D numpy array with shape `n_stepsx241x480`

### io_openaq.py

##### Description
- This file contains functions that are responsble for reading openaq data.
- The file contains only one class called `OpenAQData` and needs three argumets for initialisation.
    - `day` (str) : string date for which data is to be read
    - `span` (int) : number of days before and after the day for which the data is to be read
    - `parameter` (str) : parameter for which data is to be read. Example "pm25"
- Data can be accesed from `OpenAQData` using `.data` object

- The returned `.data` object is a 4-D list `n_stepsx241x480xn_locations`


## Scripts

### run_local.py

- It helps to create plots for data from a single grid box.
- Creates a spatial plot and a time series plot
- All that is needed is lat, lon and some specification about the method
- The script is self explanatory in iteself

### run.py

- This script helps us to write the csv files for long time and for all the grids
- The written data is can then be used to analyse further

### run_stats.py

- This script utilises the output of run.py to analyse the regional and local levels
- This script can also be utilised to get the number of stations classified differently by different methods
- The script is self explanatory in itself.