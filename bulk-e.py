import os, sys, logging
from dotenv import load_dotenv
import json
import pandas as pd
import requests

# get the file name from the script argument
files_base = "imports/" + sys.argv[1]

if len(sys.argv)-1 == 1:
  action = 'plan'
elif len(sys.argv)-1 == 2:
  if sys.argv[2] == 'plan':
    action = 'plan'
  if sys.argv[2] == 'apply':
    action = 'apply'
  if sys.argv[2] == 'destroy':
    action = 'destroy'
elif len(sys.argv)-1 > 2:
  print('too many arguments')
  exit() 

devices_file = files_base + "-devices.csv"
commons_file = files_base + "-common.csv"
logging_file = files_base + "-logging.txt" 
print(F'Devices Filename: {devices_file}')
print(F'Commons Filename: {commons_file}')
print(F'Logging Filename: {logging_file}')

devices_df = pd.read_csv(devices_file, dtype=str)
commons_df = pd.read_csv(commons_file, dtype=str)
# print(F"Shared Settings\n{commons_df}")

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

HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

path = "/devices"
url = REQ_URL + path

# Create the full import data frame
deviceimport_df = devices_df

# Add "commons" columns if not present in devices file
if 'app_eui' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(app_eui = str(commons_df['app_eui'][0]))
if 'activation' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(activation = commons_df['activation'][0])
if 'appskey' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(appskey = str(commons_df['appskey'][0]))
if 'nwkskey' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(nwkskey = str(commons_df['nwkskey'][0]))
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

if action == 'plan':
  print('===== Import Plan Only ======')

for i in range(0, len(deviceimport_df)):
  # get the row
  row=deviceimport_df.iloc[i]
  data = {}

  # prep the tags
  tags=row['tags'].split(' ')
  common_tags=row['common_tags'].split(' ')

  data['dev_eui'] = row['dev_eui'].lower()
  data['app_eui'] = row['app_eui']
  data['activation'] = row['activation'].upper()
  if data['activation'] == 'OTAA':
    data['app_key'] = row['app_key']
  elif data['activation'] == 'ABP':
    data['dev_addr'] = row['dev_addr']
    data['appskey'] = row['appskey']
    data['nwkskey'] = row['nwkskey']
  data['encryption'] = row['encryption'].upper()
  data['dev_class'] = row['dev_class'].upper()
  data['counters_size'] = int(row['counters_size'])
  data['band'] = row['band'].upper()

  adr = {}
  adr['mode'] = row['adr']
  # adr['tx_power'] = row['tx_power']
  # adr['datarate'] = row['datarate']
  data['adr'] = adr

  data['tags'] = tags + common_tags

  data_json = json.dumps(data)

  if action == 'plan':
    print(f'Plan Device {i}: {data_json}')
  elif action == 'apply':
    response = requests.post(url, data_json, params={"access_token": NS_TOKEN}, headers=HEADERS)
    if response.status_code == 201:
      # print(response.request.url)
      # print(response.request.headers)
      # print(response.request.body)
      message = F"Success: Device Added {data['dev_eui']}, Status Code: {response.status_code}, reason:{response.reason}"
      logger.info(message)
      print(message)

    else:
      # print("--------------------\nRequest Details:")
      # print(response.request.url)
      # print(response.request.headers)
      # print(response.request.body)
      message = F"Failed: Device NOT ADDED: {data['dev_eui']}, Status Code: {response.status_code}, reason:{response.reason}, text:{response.text}"
      logger.info(message)  
      print(message)
