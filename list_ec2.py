#!/usr/bin/python

import io
import sys
import json
import boto3
from botocore.exceptions import ClientError

access_key = 
secret_key = 

def get_ec2_fulldetails(region):
    ec2=boto3.client('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name=region)
    response = ec2.describe_instances()
    for instance in response["Reservations"]:
      print(instance)

def describe_security_group(id):
  ec2=boto3.client('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name=region)
  try:
    response = ec2.describe_security_groups(GroupIds=[id])
    print("Security group Description")
    return response
  except ClientError as e:
    print(e)

def cut_security_group(group):
  x = str(group)
  y = x.find('GroupId')
  x = x[y+11:len(x)]
  x = x[:x.find("'")]
  return x

def get_ec2_instances(region):
    ec2=boto3.resource('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_key,region_name=region)
    print("-----------------------"+region+"-----------------------------")
    instances = ec2.instances.filter(Filters=[{}])
    for instance in instances:
      print(instance.id, instance.instance_type, instance.vpc_id, instance.security_groups)
      sec_gp = describe_security_group(cut_security_group(instance.security_groups))
      print(sec_gp)

    '''sgs = list(ec2.security_groups.all())
    print("Security groups for " + region + ": ", sgs)
    insts = list(ec2.instances.all())
    all_sgs = set([sg.group_name for sg in sgs])
    print("Security Groups all: ", all_sgs)
    all_inst_sgs = set([sg['GroupName'] for inst in insts for sg in inst.security_groups])
    print("Security Groups attached to Instance: ", all_inst_sgs)
    unused_sgs = all_sgs - all_inst_sgs
    print("Security groups Unattached: ", unused_sgs)'''
    print("-----------------------"+region+"-----------------------------")

if __name__ == '__main__':

  if( len(sys.argv) != 2 ):
    print("Please check the arguments and try again")  
    sys.exit("exiting")
  name = sys.argv[1]
  
  regions = ['us-east-1','us-west-1','us-west-2','eu-west-1','sa-east-1','ap-southeast-1','ap-southeast-2','ap-northeast-1','ap-south-1']
  for region in regions: 
    #get_ec2_fulldetails(region)
    get_ec2_instances(region)