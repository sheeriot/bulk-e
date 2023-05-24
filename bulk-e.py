import pandas as pd
import os
import requests
import json
from dotenv import load_dotenv

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

# get the file name from the script argument

devices_file = 'import-A-devices.csv'
commons_file = "import-A-common.csv"

devices_df = pd.read_csv(devices_file)
commons_df = pd.read_csv(commons_file)

# Create the import file.
deviceimport_df = devices_df
# Only add columns not present in devices file

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
if 'common_tags' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(common_tags = commons_df['common_tags'][0])
if 'band' not in devices_df.columns:
  deviceimport_df = deviceimport_df.assign(band = commons_df['band'][0])

# Process the file one row at a time and post to NS

for i in range(0, len(deviceimport_df)):
  row=deviceimport_df.iloc[i]
  tags=row['tags'].split(',')
  common_tags=row['common_tags'].split(',')

  # print(f'tags\n{tags}')
  # print(tags)
  data = {}

  data['dev_eui'] = row['dev_eui']
  data['app_eui'] = row['app_eui']
  data['app_key'] = row['app_key']

  data['activation'] = row['activation'].upper()
  data['encryption'] = row['encryption'].upper()

  data['dev_class'] = row['dev_class'].upper()
  data['counters_size'] = int(row['counters_size'])

  adr = {}
  adr['mode'] = row['adr']
  # adr['tx_power'] = row['tx_power']
  # adr['datarate'] = row['datarate']
  data['adr'] = adr

  data['band'] = row['band']

  data['tags'] = tags + common_tags

  data_json = json.dumps(data)
  # print(data_json)

  response = requests.post(url, data_json, params={"access_token": NS_TOKEN}, headers=HEADERS)

  print(F'Server Response: {response}, {response.text}')  

  # Must build a log file
  
  # print(response.request.url)
  # print(response.request.headers)
  # print(F'Request body\n{response.request.body}')