# DAAQS
Detect Anomaly in Air Quality Station (DAAQS)

### How to run the script

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
- Run the script run.py to test. It took 1200 seconds on our machine.