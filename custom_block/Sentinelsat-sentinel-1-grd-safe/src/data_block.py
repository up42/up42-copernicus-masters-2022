import os
import os.path
import json
import geojson
import zipfile
from pathlib import Path
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from pprint import pprint
import datetime
from datetime import datetime as dt
from shapely.geometry import shape, box
from geojson import Feature, Polygon, FeatureCollection
#UP42 https://blockutils.up42.com/
from blockutils.common import BlockModes
from blockutils.logging import get_logger
from blockutils.common import encode_str_base64
from blockutils.exceptions import SupportedErrors, UP42Error

#######################################################################
# Obtaining env var to logging
def read_up42_env_variable(
    var_name: str, encode_base64: bool = False, use_block_cred: bool = False
) -> str:
    """
    https://github.com/up42/blocks-data/blob/master/libs/apiutils/up42_secrets.py
    """
    cred_path = Path("/secret/environment/")
    if use_block_cred:
        cred_path = Path("/secret/block-environment/")
    try:
        envvar_content = os.environ[var_name]
        assert envvar_content != ""
    except (KeyError, AssertionError):
        try:
            with open(cred_path / f"{var_name}", encoding="utf-8") as txt_src:
                envvar_content = txt_src.read().splitlines()[0]

        except (KeyError, FileNotFoundError) as err:
            raise UP42Error(
                SupportedErrors.INPUT_PARAMETERS_ERROR,
                f"Please set {var_name} in the UP42 environment variables!",
            ) from err
        if encode_base64:
            envvar_content = encode_str_base64(envvar_content)
    return envvar_content

#######################################################################

# Activate logger for info
logger = get_logger(__name__)

## Default input and output directories.
#INPUT_DIR="/tmp/input"
OUTPUT_DIR="/tmp/output"
params = {}
value = {}
footprint = {}
data_geo = {}

## Source the parameters from the environment.
params = json.loads(os.environ["UP42_TASK_PARAMETERS"])

value = os.environ.get("UP42_JOB_MODE", BlockModes.DEFAULT.value)
if value not in [mode.value for mode in BlockModes]:
    value = "DEFAULT"

# Check parameters & mode
#logger.info(pprint(params))
logger.info(f"Value of the job mode variable is : {value}")

# Obtain geometry of the area of interest
try:
  data_geo = params['contains']
  
  footprint = shape(data_geo)

except:
  logger.info("bbox parameters will be used")

# Obtain geometry of the area of interest
try:
  data_geo = params['bbox']

  min_x, min_y = data_geo[0], data_geo[1]
  max_x, max_y = data_geo[2], data_geo[3]
  
  # Create the polygon using Shapely
  footprint = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)

except:
  logger.info("contains parameters will be used")

# Cheking possible values that are: HH, VV, HV, VH, HH HV, VV VH
polarisationmode = params['polarization']

if '+' in polarisationmode:
    
    polarisationmode = (params['polarization'].rsplit('+', 1)[0] + " " + params['polarization'].rsplit('+', 1)[1])
else:
    
    polarisationmode = params['polarization']

# Start time
startdate = datetime.datetime.strptime(dt.strftime(dt.strptime(params['time'].rsplit('/', 1)[0].rsplit('+', 1)[0], '%Y-%m-%dT%H:%M:%S'),  '%Y-%m-%d'), "%Y-%m-%d")

# End time
enddate = datetime.datetime.strptime(dt.strftime(dt.strptime(params['time'].rsplit('/', 1)[1].rsplit('+', 1)[0], '%Y-%m-%dT%H:%M:%S'),  '%Y-%m-%d'), "%Y-%m-%d")

# Environment variables across workflows
user = read_up42_env_variable("USER")
password = read_up42_env_variable("PASSWORD")

# Activate session
api = SentinelAPI(user, password)

# Results from SentinelSat
products = api.query(footprint, producttype = "GRD", date = (startdate, enddate), identifier = params['ids'], orbitdirection = params['flightDirection'], polarisationmode = params['polarization'], orbitnumber = params['orbitnumber'], limit = params['limit'])

# Print information from results
logger.info(products)

# Handle the serialization correctly
json_object = api.to_geojson(products)

# Check if Dry Run or Live Job
if value == "DRY_RUN":
    # Printing info
    logger.info("Beginning authentication process")

    # Printing info
    logger.info(api)

    # Count of total files search
    logger.info(f"The download of the data.json for {str(params['limit'])} scene(s) will be started")

    for i in range(params['limit']):
            
        # Add up42.data_path
        if 'contains' in params:
            json_object['features'][i]['contains'] = data_geo
            json_object['features'][i]['properties']["up42.data_path"] = json_object['features'][i]['properties']["identifier"]

        else:
            json_object['features'][i]['bbox'] = data_geo
            json_object['features'][i]['properties']["up42.data_path"] = json_object['features'][i]['properties']["identifier"]

    # Save data.json
    with open('/tmp/output/data.json', 'w') as f:
        json.dump(json_object, f)

else:

    # Printing info
    logger.info("Beginning authentication process")

    if params['provider'] == "SENTINELSAT":

        # Printing info
        logger.info(api)
        
        # Count of total files search
        logger.info(f"The download of {str(params['limit'])} scene(s) will be started")

        # Change directory from working dir to dir with files
        os.chdir(OUTPUT_DIR)
        
        # Download images
        api.download_all(products)

        # Download
        for i in range(params['limit']):

            # Add up42.data_path
            if 'contains' in params:
                json_object['features'][i]['bbox'] = data_geo
                json_object['features'][i]['properties']["up42.data_path"] = json_object['features'][i]['properties']["identifier"]

            else:
                json_object['features'][i]['bbox'] = data_geo
                json_object['features'][i]['properties']["up42.data_path"] = json_object['features'][i]['properties']["identifier"]

            # Unzip the file to get the .SAFE
            extension = ".zip"

            #Make a folder
            os.mkdir(json_object['features'][i]['properties']["identifier"])

            filepath = "/tmp/output/" + json_object['features'][i]['properties']['identifier'] + extension

            # Unzip files and erase .zip
            zip_ref = zipfile.ZipFile(filepath) # create zipfile object
            zip_ref.extractall(json_object['features'][i]['properties']["identifier"]) # extract file to dir
            zip_ref.close() # close file
            os.remove(filepath) # delete zipped file
        
        # Save data.json
        with open('/tmp/output/data.json', 'w') as f:
            json.dump(json_object, f)

    else:
        # Error for credentials to logging
        raise UP42Error(
            SupportedErrors.INPUT_PARAMETERS_ERROR,
            "Parameter for logging must be 'SentinelSat'",
        )
    
    # Inform that the process has been finished
    logger.info("The image(s) has(have) been downloaded")