import os, sys, logging
from dotenv import load_dotenv
import json
import pandas as pd
import requests

# get the file name from the script argument
files_base = "imports/" + sys.argv[1]

devices_file = files_base + "-devices.csv"
commons_file = files_base + "-common.csv"
logging_file = files_base + "-logging.txt" 
print(F'Devices Filename: {devices_file}')
print(F'Commons Filename: {commons_file}')
print(F'Logging Filename: {logging_file}')

devices_df = pd.read_csv(devices_file)
commons_df = pd.read_csv(commons_file)

logging.basicConfig(filename=logging_file, 
					format='%(asctime)s %(message)s', 
          datefmt='%Y-%m-%d %H:%M:%S',
					filemode='a') 

# Create a logging object 
logger=logging.getLogger() 
# Set the threshold of logger to DEBUG 
logger.setLevel(logging.INFO)
# Print a log message 
logger.info('----------------------------------')
logger.info(F"Import Initiated! {sys.argv[1]}") 

load_dotenv()
NS_TOKEN = os.getenv('NS_TOKEN')

HTTP_SCHEMA = "https://"
BASEURL = "ns.us.everynet.io"
BASEPATH = "/api/"
API_VERSION = "v1.0"
REQ_URL = HTTP_SCHEMA + BASEURL + BASEPATH + API_VERSION

HEADERS = {"accept": "application/json", "Content-Type": "application/json"}

path = "/devices"
url = REQ_URL + path

# Create the full import data frame
deviceimport_df = devices_df

# Add "commons" columns if not present in devices file
if 'activation' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(activation = commons_df['activation'][0])
if 'encryption' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(encryption = commons_df['encryption'][0])
if 'dev_class' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(dev_class = commons_df['dev_class'][0])
if 'counters_size' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(counters_size = commons_df['counters_size'][0])
if 'adr' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(adr = commons_df['adr'][0])
if 'tx_power' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(tx_power = commons_df['tx_power'][0])
if 'datarate' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(datarate = commons_df['datarate'][0])
if 'band' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(band = commons_df['band'][0])
if 'common_tags' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(common_tags = commons_df['common_tags'][0])

# Process the import dataframe, create device (post) at NS
for i in range(0, len(deviceimport_df)):
  # get the row
  row=deviceimport_df.iloc[i]
  data = {}

  # prep the tags
  tags=row['tags'].split(',')
  common_tags=row['common_tags'].split(',')

  data['dev_eui'] = row['dev_eui'].lower()
  data['app_eui'] = row['app_eui'].lower()
  data['app_key'] = row['app_key'].lower()
  data['activation'] = row['activation'].upper()
  data['encryption'] = row['encryption'].upper()
  data['dev_class'] = row['dev_class'].upper()
  data['counters_size'] = int(row['counters_size'])
  data['band'] = row['band']

  adr = {}
  adr['mode'] = row['adr']
  # adr['tx_power'] = row['tx_power']
  # adr['datarate'] = row['datarate']
  data['adr'] = adr

  data['tags'] = tags + common_tags

  data_json = json.dumps(data)
  # print(data_json)

  response = requests.post(url, data_json, params={"access_token": NS_TOKEN}, headers=HEADERS)
  if response.status_code == 201:
    logger.info(F"Add Device Result: {data['dev_eui']}, Status Code: {response.status_code}, reason:{response.reason}")
  else:
    logger.info(F"BAD Device Result: {data['dev_eui']}, Status Code: {response.status_code}, reason:{response.reason}, text:{response.text}")  

