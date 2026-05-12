"""
Created on Sun Apr 19 14:01:43 2026

@author: noriega

An alerter using nobitex API (test). i used test api bcaz we dont want to do the banking things 
and auth to get access to the token.
you can replace the real API with test API at <NOBITEX_API_BASE_PATH>.
In this project i used KavehNegar sms webservice you can use 
every web service you like but you have to call the webserivce's API that you are using and put your 
API-KEY at <KN_API_KEY> or even change the variable name.
"""


import argparse
import requests
import time 
# Configuration 

KN_API_KEY = "<KAVEH_NEGAR_API_KEY>"
KN_SENDER = "2000660110"
NOBITEX_API_BASE_PATH = "https://testnetapiv2.nobitex.ir/v2/depth/"


# Getting Prices from Nobitex API 

def getPrice(symbol : str ):
    NOBITEX_FULL_PATH = NOBITEX_API_BASE_PATH + symbol.upper()
    print(f"[+] Fethcing Price From {NOBITEX_FULL_PATH}")
    try :
        response = requests.get(NOBITEX_FULL_PATH , timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        #print(f"[DEBUG] Full API Response JSON for {symbol}: {data}")
        
        priceStr = data.get("lastTradePrice")
        if priceStr is None:
            print(f"[ERROR] 'lastTradePrice' key not found in response for {symbol}.")
            return None
            
        price = float(priceStr)
        #print(f"[DEBUG] Successfully parsed price for {symbol}: {price}")
        return price
        
        #print(f"[DEBUG] Full API Response JSON for {symbol}: {price}")
        #print(data)
        
    except requests.exceptions.Timeout :
        print(f"Oops: Request to Nobitex API timed out for {symbol} :( .")
        return None
    
# Sends an SMS alert via Kavenegar

def smsALert(receptor : str ,message : str) :
    if not KN_API_KEY :
        print("Oops! sms API-KEY is not configured.You have to set your API-KEY in case to send sms. ")
        
    receptorStr = str(receptor) #Parameter : Receptor , Type : String (KavehNegar Documentation)
    messageStr = str(message) #Parameter :  Message , Type : string (KavehNegar Documentation)
        
    KN_API_PATH = f'https://api.kavenegar.com/v1/{KN_API_KEY}/sms/send.json?receptor={receptorStr}&sender={KN_SENDER}&message={messageStr}&tag=Alert' 
    
    response = requests.get(KN_API_PATH)
    result = response.json()
    try :
        
        if result or '200' in result['status'] or 'تایید شد' in result['message'] :
            print(f"Message Successfully sent to {receptorStr} :)")
        else :
            print("Oops ! Something Happend with KavehNegar")
    except requests.exceptions.Timeout : 
        print(f"Oops: Request to KavehNegar API timed out for Message {messageStr} :( .")

"""
main logic of this project. every alert request should be a set of SYMBOL,OPERATOR,VALUE,RECEPTOR.So now we have
to validate the alert command and validate the operators and last but not least sending the sms. Variable Value 
is the threshold that you will determine.
"""
def process_alerts(alerts) :
    for alert in alerts :
        parts = [p.strip() for p in alert.split(",")]
        if len(parts) < 3 or len(parts) > 4 :
            print("[-] Invalid Alert Format")
            continue
        symbol , operator , value_str , receptor = parts
        value = float(value_str)

        price = getPrice(symbol)
        if price is None:
            print(f"[-] Failed to retrieve price for {symbol}. Cannot evaluate alert.")
            # Continue to the next alert instead of returning
            continue

        OpIsTrue = False
        if operator == ">" :
            OpIsTrue = price > value
        elif operator == "<" :
            OpIsTrue = price < value
        elif operator == ">=" :
            OpIsTrue = price >= value
        elif operator == "<=" :
            OpIsTrue = price <= value
        elif operator == "==" :
            OpIsTrue = price == value
        else :
            print("Unsupported Operator help : use [>],[<],[>=],[<=],[==]")
            continue # Skip to next alert if operator is unsupported

        if OpIsTrue :
            msg = f'قیمت {symbol} برابر است با {price} (ریال) که {operator} است با حد تعیین شده شما'
            smsALert(receptor, msg)

            
        

def main() :
    parser = argparse.ArgumentParser(
        prog='NobitexAlerter' ,
        description='Monitoring tool using nobitex API (test) which will monitor the prices and alert the user with sms'
        )

    parser.add_argument(
        '--alert' , '-a',
        action='append' , 
        help='define a customized alert ===> <SYMBOL>,<OPERATOR>,<VALUE>,<RECIPTOR>'
        )
    
    parser.add_argument(
        '--duration' , '-d',
        type=int , 
        default=15 #minutes
        
        )
    
    parser.add_argument(
        '--sleep' , '-s',
        type=int , 
        default=300 #seconds (5 minutes)
        
        )
    args = parser.parse_args()
    
    
    
    #continous monitoring with a while loop 
    
    startTime = time.time()
    endTime = startTime + (args.duration * 60)
    print(f'[+] starting monitoring continunous for {args.duration} (minute) with {args.sleep} (second) interval')    
    
    while time.time() < endTime:
        
        process_alerts(args.alert)
        
        if time.time() < endTime:
            print(f"[*] Waiting for {args.sleep} seconds before next check . . . ")
            time.sleep(args.sleep)
            
if __name__ == "__main__":
    main()    
