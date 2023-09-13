import requests
import random
import pandas as pd
import os

def get_symbol(api_key):

    topGainers_url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}'

    topResponse = requests.get(topGainers_url)
    if topResponse.status_code == 200:

        data = topResponse.json()
        topGainers_Data = data['top_gainers']
 
        random_company_index = random.randint(0,len(topGainers_Data) -1)
        selected_company = topGainers_Data[random_company_index]

        return selected_company

    else:
        print(f"Error: Status Code {topResponse.status_code} was returned in get_symbol.")
        return False


def get_company_details(company_object,api_key):

    comp_symbol = company_object['ticker']
    # check or and remove the '+' at the end
    
    if comp_symbol[len(comp_symbol) -1 ] == '+':
        comp_symbol = comp_symbol[:len(comp_symbol)-1]
   
    
    company_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={comp_symbol}&apikey={api_key}'

    comp_response = requests.get(company_url)
   
    if comp_response.status_code == 200:

        return comp_response.json()
       
        

    else:
        print(f"Error: Status Code {comp_response.status_code} was returned  in get_company_details.")
        return False



def get_daily_data(comp_object,api_key):

    current_dir = os.path.dirname(__file__)
    monthlycsv_path = os.path.join(current_dir, "monthly_data.csv")


    comp_symbol = comp_object['Symbol']

    monthly_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={comp_symbol}&apikey={api_key}&datatype=csv'

    monthly_response = requests.get(monthly_url)
    if monthly_response.status_code == 200:
        fp = open(monthlycsv_path, 'w+')
        print(monthly_response)
        fp.write(monthly_response.text)
        return True
    else:
        print(f"Error: Status Code {monthly_response.status_code} was returned in get_monthly_data")
        False



def get_data(api_secret):

    todays_company = get_symbol(api_secret)
    if todays_company == False or todays_company == {}:
        print(todays_company)
        print( "Error Has Occured While Scraping A Company From the Top Winners Chart")
        return None, None
    

    com_datails = get_company_details(todays_company,api_secret)
    if com_datails == False or com_datails == {}:
        print(com_datails)
        print( f"Error Has Occured While Scraping {todays_company} Details")
        return None, None

  
    if get_daily_data(com_datails,api_secret) == False:
        print( "Error Has Occured While Writing Historical Data to a CSV File")
        return None, None
    
    return todays_company, com_datails['Name']




