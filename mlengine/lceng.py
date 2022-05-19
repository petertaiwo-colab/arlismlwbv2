# from MLWB.mlengine.tests import geturl
import pandas as pd
import os
import json
import zipfile
import csv
import base64
import io, random, subprocess
from PIL import Image
from datasearch.models import Usersessn, Admintrack
from datetime import datetime

import boto3, json, time
client = boto3.client('sagemaker', region_name='us-west-2')
# client = boto3.client('sagemaker')
rnow = datetime.now().strftime('-%Y-%m-%d-%H-%M-%S')

def getport():
    try:
        ins = Admintrack.objects.get(id=0)
    except:
        ins = Admintrack(id=0)
    port = random.choice([x for x in range(8800,8899) if x not in ins.jport])
    ins.jport.append(port)
    ins.save()
    print(ins.jport)
    return port


def lclnb(user, vmtype):
    obj = Usersessn.objects.get(user=user) 
    port = str(getport())    
    # ins = Admintrack.objects.get(id=0) 
    instname = user+rnow+'-'+port
    print(instname)
    obj.lclnb['instname'] = instname
    url, responsetime, setuptime = opennb(port, vmtype)
    # print(response)
    obj.lclnb['vmtype'] = 'Local Machine CPU+GPU'
    obj.lclnb['setuptime'] = setuptime    
    obj.lclnb['insturl'] = url
    # print(auth_url)
    obj.save()

    # jupyter notebook --no-browser --ip 192.168.1.214 --port 8890

def opennb(port, vmtype):
    ttic = time.time()
    cmd = ['jupyter', 'notebook', '--no-browser', '--ip', '192.168.1.214', '--port '+port]
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='/home/pt/s3-bucket/MLWB/petai1test')
    responsetime = time.time() - ttic
    url = geturl(port)
    setuptime = time.time() - ttic
    return url, responsetime, setuptime

def geturl(port):
    while True:
        cmd1 = ['jupyter', 'notebook', 'list']
        p1 = subprocess.run(cmd1, capture_output=True, text=True)
        cmd2 = ['grep', port]
        p2 = subprocess.run(cmd2, capture_output=True, text=True, input=p1.stdout)
        nbstatus = 'InService'      
        try: 
            url = p2.stdout.split()[0]         
            print(url)
        except:
            nbstatus = 'Pending'
            print(nbstatus)
        if nbstatus == 'InService':
            print(nbstatus)
            break
    # cmd1 = ['jupyter', 'notebook', 'list']
    # p1 = subprocess.run(cmd1, capture_output=True, text=True)
    # cmd2 = ['grep', port]
    # p2 = subprocess.run(cmd2, capture_output=True, text=True, input=p1.stdout)
    return url

