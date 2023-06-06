## This tool for provisioning device in Everynet Network Server

Post Device API is here

* https://ns.docs.everynet.io/management/devices.html#/Device/create_device

```
{
  "dev_eui": "cb105012c80769f7",
  "app_eui": "d66a26096626ca12",
  "tags": [],
  "activation": "ABP",
  "encryption": "NS",
  "dev_addr": "6c89893f",
  "nwkskey": "edf2ff46452491424cf15f0d9a29588f",
  "appskey": "1c8a76070844d1d7a5e5e29f97f28686",
  "dev_class": "A",
  "counters_size": 4,
  "adr": {
    "tx_power": null,
    "datarate": null,
    "mode": "on"
  },
  "band": "EU863-870"
}
```

## Bulk-E Device Add Setup

This section provides brief instructions for setting up the Bulk-E Device Add script.

Setup of Python is outside the scope of this readme.

If using windows, go here:
* https://www.digitalocean.com/community/tutorials/install-python-windows-10

### Device and Commons CSV Files

Create two (2) files for each import group.

1. {importName}-commons.csv - contains the shared parameters
1. {importName}}-devices.csv - list of devices with unique values

### Setup .env
The access_token (created at the Everynet Network Server) with rights to create Devices. This is stored in a hidden file named `.env` for the local setup.

`.env`
``` 
NS_TOKEN=xxxxx
```

### Run the Script

Pass the "Import Name" to the python script. 

e.g.
```
# python bulk-e.py runX

Devices Filename: imports/runX-devices.csv
Commons Filename: imports/runX-common.csv
Logging Filename: imports/runX-logging.txt
```

### Notes

1. if not in the US, edit the URL on line 37 for your Network Server (NS) URL
1. 
1. Activation by OTAA and ABP are implemented.
2. OTAA needs AppKey. ABP needs NwkSKey, AppSKey, Dev_Addr
3. ADR Static settings for "datarate" and "tx_power" are not yet implemented




