### Part 1 - Data Ingestion
#### Assumptions
1. This pipeline is to be run via Postgresql
2. The following software/tools must be set up:
* Python3 (version that was used for this tutorial is 3.10.6 - most latest as of Aug. 2, 2022)
* PostgreSQL
3. The database environment must be set up so it is able to accept connections; includes the following requirements but not limited to:
* Database environment such as Google Cloud Database or Amazon RDS instance to be set up
* Postgresql engine (For this example)
* Be publicly accessible (if private, allow traffic from the environment the pipeline will be set up)
* Have a connectable and loadable database (on the SQL instance)
4. The input data, sample_data.csv, will be placed/updated in the same designated local/network folder at the user's designated frequency (for example, every one hour)
5. The input data's data formats (e.g. SeriousDlqin2yrs, age) will remain constant
6. The input data, sample_data.csv, will be replacing the existing sample_data.csv at the designated frequency
7. The nomenclature of the created table in the database will change on a daily basis; any new update within the same on the sample_data.csv will be reflected on the next upcoming Cronjob


#### Setup Procedures
1. Edit the YAML file (./conf/config.yaml) depending on the environment the pipeline will be set up (see ./conf/config.yaml file on how to edit the fields)
2. Open Terminal and cd (change directory) to where the pipeline folder (ie. part1) is located
3. Run the pipeline setup script by typing **sh setup.sh** (make sure to have the pre-required software/tools to be installed) and press Return/Enter
4. Run the pipeline script by typing **sh run.sh** and press Return/Enter - this will kick off the ETL pipeline based on the details filled in YAML file
5. To run the pipeline at the designated frequency (every one hour), we use Cronjob to run the pipeline script shell. Open Terminal again and set up the Cronjob (see Cronjob details below or refer to the Cron documentation)


#### Cronjob activation
The following procedures are in order to set up the pipeline activation at a designated frequency.
1. Open Terminal
2. Type **crontab -e** and press Return/Enter
3. Press **i** in order to enter Crontab editor mode
4. Type the desired Crontab configuration. For instance, if we want to set up the pipeline activation to run for every hour it will be as the following:

> \*\ */1 * * * ./path1/subpath1/.../part1/run.sh

Explanation: The above configuration is configured in Crontab **./path1/subpath1/.../part1/run.sh** every 1 hour (starting at the next minute once configured in Crontab) and will log on **./path1/subpath1/.../part1/log/sch_run.log**.

5. After the above Crontab configuration has been typed, press Esc(ape) and type **:wq** to overwrite onto the existing Crontab configuration

As an alternative, a single liner of

> crontab -l | { cat; echo "* */1 * * * ./path1/subpath1/.../part1/run.sh"; } | crontab -

also works via Terminal.


#### File/Folder(s) explanation
* conf: configuration files such as connections, credentials, directory
* src: pipeline code
* utils: miscellaneous code such as transformation and validation
* data: contains data
* log: contains logs
* setup.sh: script to initiate pipeline deployment setup
* run.sh: script to initiate pipeline; can be used individually directly via Terminal or via Cronjob
* test_query.R: R script to test whether loaded table can be queried via R language
* requirements.txt: text file that contains all modules required for setup.sh


#### Pipeline workflow
1. Imports necessary modules and functions that are relevant towards the ETL
2. Reads configuration data from **config.yaml**
3. Locates/extracts file to be uploaded
4. Transforms data as required, according to business needs
5. Validates data as required, according to business rules
6. Connects to database according to the configuration data read from step 2
7. Checks if table exists
8. If table exists, then new data will be appended; else, table will be created and data that has been extracted will be loaded
