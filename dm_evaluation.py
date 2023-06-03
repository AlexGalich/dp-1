import requests
from bs4 import BeautifulSoup
from dmarket_info import encode_item
import csv 
import json


def request_sales_history(item_encoded):
    header = {'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlNjE5N2Y4Yi1iMTVhLTQ0MmMtYWZmYi0yYmM0ZThkMWJkZTkiLCJleHAiOjE2ODU2MzgxMDMsImlhdCI6MTY4MzA0NjEwMywic2lkIjoiNzNlMGVlMzQtNmI3ZC00ZWM4LTgyMjktN2UzMjI2MzM1NDZjIiwidHlwIjoiYWNjZXNzIiwiaWQiOiIxNjViMWE3Yy1kZDZmLTQ0YzYtYjI2MC02OGU1NTA4OTFiMTAiLCJwdmQiOiJtcCIsInBydCI6IjIzMDUiLCJhdHRyaWJ1dGVzIjp7InNhZ2Ffd2FsbGV0X2FkZHJlc3MiOiIweDEwMGYzZTBkMGRENGFCMTc0MmZFZUYyMDc3NzA0RTcyMzRjNWZiZGMiLCJhY2NvdW50X2lkIjoiMzZjOWM5MTMtZDBhZC00ZGNjLTk0NTMtMTI0YjJmMTQ4ZTk5Iiwid2FsbGV0X2lkIjoiNzZhZjAyNTkyYzNkZGZkMWQ0YWU5NmZiZDU2YzhkYmY5ZWY4ZmU1NTAyNmVkYmUyODgzMGIyYTdlNzE5NGRlMyJ9fQ.ZC5edMIOC4YR7dWhjvNime96rKCm2kPxswskI1wiceENzRKmJBFwKsAXUUz26zv1YOw7A8ACtia3OLTX6emTaQ'}
    market_response = requests.get(f'https://api.dmarket.com/marketplace-api/v1/sales-history?Title={item_encoded}&GameID=a8db&Period=7D&Currency=USD',headers=header)
    try:
        hist = json.loads(market_response.text)
      
        return hist['SalesHistory']
    
    except:
        return None
    

def check_amount_criterias(item_info):
    if item_info == None:
        return False 
    
    else:
        higher_15 = all(i >= 7 for i in item_info['Items'])
        if higher_15 :
            return True 
        else :
            return False
def check_price_criteria(item_info):
    # Get sale price in cents , convert them from str to int
    
    price_list = item_info['Prices']
    if '' in price_list:
        return False


    item_prices = [eval(i) for i in item_info['Prices']] 
   
    avg_prices = sum(item_prices)/ len(item_prices)
       
    if 500 <= avg_prices >= 25:
            return True 
    return False 

       



def calculate_dm_signal(item_name):


    encoded_item = encode_item(item_name)

    item_infos = request_sales_history(encoded_item)
    amount_criteria = check_amount_criterias(item_infos)
    price_criteria = check_price_criteria(item_infos)
    

    if amount_criteria and price_criteria :
        return True 
    return  False





