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

Two files for setup.

1. import{ID}-common.csv - contains common parameters
1. import{ID}-devices.csv - list of devices with values

API key be collected during run. Keeps it out fo file system and shell history.

