# pensacola-verification

Verification of Cloudrun forecasts for the Pensacola region

## Getting started

### Clone this repo

```
git clone git@github.com:cloudruninc/pensacola-verification
```

### Set up a Python environment

```
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -U -r requirements.txt
```

or equivalent with conda.

### Set environment variables

You need to set these environment variables to download Cloudrun data:

* `CLOUDRUN_API_TOKEN`
* `CLOUDRUN_USER_ID`

### Download the data

```
python3 download_data.py
```

It will take a while. Once done, the data will be available at:

```
data/
  PNS_2019111100/
  PNS_2019111112/
  PNS_2019111200/
  PNS_2019111212/
  ...
```
