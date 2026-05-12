# NobitexPriceAlerter
A lightweight Python alerting tool that monitors a cryptocurrency symbol on Nobitex and sends SMS alerts when a price crosses or equals  your chosen threshold.
this project uses the Nobitex test API and can send notifications through Kavenegar SMS. It is designed to be simple, extendable, and easy to adapt to other APIs.

# Project Structure 
```text
NobitexAlerter/
├── NobitexAlerter.py
├── README.md
└── requirements.txt
```

# Features
* Monitors crypto prices from Nobitex test API.

* Supports multiple alerts from the command line.

* Checks price against custom thresholds.

* Sends SMS notifications through Kavenegar.

* Configurable polling interval and monitoring duration.

* Easy to modify for other SMS providers or exchanges.

# How it works
You define alerts in this format:
```bash
SYMBOL,OPERATOR,VALUE,RECIPIENT
```
# Example 
```bash
BTCUSDT,>=,400000000,09xxxxxxxxx
```
# Configuration 
Before running the script set your API keys inside the code 
```python
KN_API_KEY = "<KAVEH_NEGAR_API_KEY>"
KN_SENDER = "2000660110"
NOBITEX_API_BASE_PATH = "https://testnetapiv2.nobitex.ir/v2/depth/"
```
# Requirements
```bash
pip install -r requirements.txt
```
# Usage
### Run one Alert
```bash
python3 NobitexAlerter.py --alert BTCUSDT,>=,400000000,09xxxxxxxxx
```
### Run multiple Alerts 
```bash
python3 NobitexAlerter.py \
  --alert BTCUSDT,>=,400000000,09xxxxxxxxx \
  --alert ETHUSDT,<=,200000000,09yyyyyyyyy
```
### Set monitoring duration and interval
```bash
python NobitexAlerter.py --alert BTCUSDT,>=,400000000,09xxxxxxxxx --duration 30 --sleep 300
```
### Arguments
* --alert or -a: Add an alert in the format SYMBOL,OPERATOR,VALUE,RECIPIENT.

* --duration or -d: Total monitoring time in minutes. Default is 15.

* --sleep or -s: Time between checks in seconds. Default is 300.

### Supported Operators
*>

*<

*>=

*<=

*==
