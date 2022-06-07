import os
import json
import geojson
import zipfile
from pathlib import Path
import asf_search as asf
from pprint import pprint
from datetime import datetime as dt
from shapely.geometry import shape, box
from geojson import Feature, Polygon, FeatureCollection
#UP42 https://blockutils.up42.com/
from blockutils.common import BlockModes
from blockutils.logging import get_logger
from blockutils.common import encode_str_base64
from blockutils.exceptions import SupportedErrors, UP42Error

#######################################################################

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
poly = {}
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
  
  poly = shape(data_geo)

except:
  logger.info("bbox parameters will be used")

try:
  data_geo = params['bbox']

  min_x, min_y = data_geo[0], data_geo[1]
  max_x, max_y = data_geo[2], data_geo[3]
  
  # Create the polygon using Shapely
  poly = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)

except:
  logger.info("contains parameters will be used")

if params['ids'] == None:

    # Results from Alaska
    results = asf.search(platform = "S1",beamMode = params['beamMode'], processingLevel = ['GRD_HS', 'GRD_HD', 'GRD_MS', 'GRD_MD'], intersectsWith = poly, start = dt.strftime(dt.strptime(params['time'].rsplit('/', 1)[0].rsplit('+', 1)[0], '%Y-%m-%dT%H:%M:%S'),  '%Y-%m-%dT%H:%M:%SZ'), end = dt.strftime(dt.strptime(params['time'].rsplit('/', 1)[1].rsplit('+', 1)[0], '%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%SZ'), flightDirection = params['flightDirection'], polarization = params['polarization'], relativeOrbit = params['relativeOrbit'], maxResults = params['limit'])

else:
    # Results from Alaska
    results = asf.search(granule_list = params['ids'])

# Handle the serialization correctly
json_object = results.geojson()

# Check if Dry Run or Live Job
if value == "DRY_RUN":
    # Printing info
    logger.info("Beginning authentication process")

    # Count of total files search
    logger.info(f"{str(params['limit'])} image(s) have been found for your project")

    for i in range(params['limit']):
            
        # Add up42.data_path
        if 'contains' in params:
            json_object['features'][i]['contains'] = data_geo
            json_object['features'][i]['properties']["up42.data_path"] = json_object['features'][i]['properties']['fileName'].rsplit('.', 1)[0]

        else:
            json_object['features'][i]['bbox'] = data_geo
            json_object['features'][i]['properties']["up42.data_path"] = json_object['features'][i]['properties']['fileName'].rsplit('.', 1)[0]

    # Save data.json
    with open('/tmp/output/data.json', 'w') as f:
        json.dump(json_object, f)

    for p in range(len(results)):
        logger.info(json_object['features'][p]['properties']['fileName'].replace('.zip',''))

else:

    # Printing info
    logger.info("Beginning authentication process")

    if params['provider'] == "ASF":

        # Environment variables across workflows
        user = read_up42_env_variable("USER")
        password = read_up42_env_variable("PASSWORD")

        # Activate session
        session = asf.ASFSession()
        work = session.auth_with_creds(user, password)
        
        # Count of total files search
        logger.info(f"The download of {str(params['limit'])} scene(s) will be started")

        # Change directory from working dir to dir with files
        os.chdir(OUTPUT_DIR)
        
        # Download images
        results.download(path = OUTPUT_DIR, session = session)

        # Download
        for i in range(params['limit']):

            # Add up42.data_path
            if 'contains' in params:
                json_object['features'][i]['bbox'] = data_geo
                json_object['features'][i]['properties']["up42.data_path"] = json_object['features'][i]['properties']['fileName'].rsplit('.', 1)[0]

            else:
                json_object['features'][i]['bbox'] = data_geo
                json_object['features'][i]['properties']["up42.data_path"] = json_object['features'][i]['properties']['fileName'].rsplit('.', 1)[0]

            #Make a folder
            os.mkdir(json_object['features'][i]['properties']['fileName'].rsplit('.', 1)[0])

            filepath = "/tmp/output/" + json_object['features'][i]['properties']['fileName']

            # Unzip files and erase .zip
            zip_ref = zipfile.ZipFile(filepath) # create zipfile object
            zip_ref.extractall(json_object['features'][i]['properties']['fileName'].rsplit('.', 1)[0]) # extract file to dir
            zip_ref.close() # close file
            os.remove(filepath) # delete zipped file
        
        # Save data.json
        with open('/tmp/output/data.json', 'w') as f:
            json.dump(json_object, f)

        for p in range(len(results)):
            logger.info(json_object['features'][p]['properties']['fileName'].replace('.zip',''))

    else:
        # Error for credentials to logging
        raise UP42Error(
            SupportedErrors.INPUT_PARAMETERS_ERROR,
            "Parameter for logging must be 'ASF'",
        )
    
    # Inform that the process has been finished
    logger.info("The image(s) has(have) been downloaded")