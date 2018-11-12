#!/usr/bin/env python3

import boto3
import json

client = boto3.client('ec2', region_name='us-east-1')

ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

tag_name = ""


def get_number_instances():
  """
    Return number of ec2 instances across AWS
  """
  ec2_count = 0

  for region in ec2_regions:
      conn = boto3.resource('ec2', region_name=region)
      instances = conn.instances.filter()
      for instance in instances:
        if instance.state["Name"] == "running":
          ec2_count+=1

  return ec2_count

def set_lambda_return_format(event, context):
    """
        Lambda function response must return in the following format
    """
    return {
      "isBase64Encoded": False,
      "statusCode": 200,
      "body": json.dumps({'value': get_number_instances() })
    }