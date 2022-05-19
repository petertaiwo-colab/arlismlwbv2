import pandas as pd
import os
import json
import zipfile
import csv
import base64
import io
from PIL import Image
from datasearch.models import Usersessn
from datetime import datetime

with open('/home/pt/awskey.csv','r')as input:    
    reader = csv.reader(input)
    key = [x[0].split('=')[1] for x in reader]    
    access_key_id = key[0]
    secret_access_key = key[1]

import boto3, json, time
client = boto3.client('sagemaker', region_name='us-west-2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
# client = boto3.client('sagemaker')
rnow = datetime.now().strftime('-%Y-%m-%d-%H-%M-%S')

def sgmk(user, vmtype):
    obj = Usersessn.objects.get(user=user) 
    print(user+rnow)
    instname = user+rnow
    obj.sgmk['instname'] = instname
    response, responsetime, setuptime = opensage(instname, vmtype)
    obj.sgmk['vmtype'] = vmtype
    obj.sgmk['setuptime'] = setuptime    
    auth_url = geturl(instname)
    obj.sgmk['insturl'] = auth_url
    print(auth_url)
    obj.save()

def opensage(instname, insttype):
    ttic = time.time()
    response = client.create_notebook_instance(
        NotebookInstanceName=instname,
        InstanceType=insttype,
        RoleArn='arn:aws:iam::341238572323:role/service-role/AmazonSageMaker-ExecutionRole-20201116T152275',
        Tags=[
            {
                'Key': 'NoteInstance',
                'Value': 'aws'
            },
        ],
        DefaultCodeRepository = "https://github.com/petertaiwo-colab/FirestoreCVDemo.git"
    )
    responsetime = time.time() - ttic
    while True:
        time.sleep(5)
        response = client.list_notebook_instances(
            NameContains=instname
        )
        nbstatus=response["NotebookInstances"][0]["NotebookInstanceStatus"]
        print(nbstatus)
        if nbstatus == "InService":
            break
    setuptime = time.time() - ttic
    return response, responsetime, setuptime

def geturl(instname):
    response = client.create_presigned_notebook_instance_url(
        NotebookInstanceName=instname
        )
    # return (json.dumps(response['AuthorizedUrl'], indent=1, default=str))
    return response['AuthorizedUrl']
