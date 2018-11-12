#!/usr/bin/env python3

import boto3
import json
import requests
from datetime import datetime, timedelta

#session = boto3.session.Session(profile_name='personal')
client = boto3.client('ce', region_name='us-east-1')

datetoday = datetime.now()
firstdateofmonth = datetoday.replace(day=1)

def get_date_today():
    """
        Return the date today in YEAR-MONTH-DAY format
    """
    time_now = datetime.now()
    return str(time_now.strftime("%Y-%m-%d"))

def get_first_of_month():
    """
        Return the first day of the current month in YEAR-MONTH-DAY format
    """
    time_now = datetime.now().replace(day=1)
    return str(time_now.strftime("%Y-%m-%d"))

def get_aws_monthly_billing():
    """
        Return the monthly AWS cost in USD
    """

    response = client.get_cost_and_usage(

        TimePeriod={
            'Start':str(firstdateofmonth.strftime("%Y-%m-%d")),
            'End':  str(datetoday.strftime("%Y-%m-%d"))
        },
        Granularity='MONTHLY',
        Metrics=[
        'BlendedCost',
        ],
    )

    return response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']

def get_gbp_exchange_rate():
    """
        Return the current USD to GBP exchange rate.
    """
    response = requests.get('http://free.currencyconverterapi.com/api/v5/convert?q=USD_GBP&compact=y')
    response = response.json()
    return response['USD_GBP']['val']

def get_aws_monthly_billing_gbp():
    """
        Return the current months cost from the first
        of the current month in GBP
    """

    return float(get_aws_monthly_billing()) * get_gbp_exchange_rate()

def set_lambda_return_format(event, context):
    """
        Lambda function response must return in the following format
    """
    return {
      "isBase64Encoded": False,
      "statusCode": 200,
      "body": json.dumps({'value': get_aws_monthly_billing_gbp() })
    }
