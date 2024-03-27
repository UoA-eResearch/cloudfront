#!/usr/bin/env python3

from netaddr import IPNetwork
import requests
from requests.exceptions import Timeout
from tqdm.auto import tqdm
from tqdm.contrib.concurrent import thread_map
import pandas as pd
import os

network = list(IPNetwork("65.9.141.27/24"))
print(f"Scanning {network[0]} to {network[-1]}")

def check_ip(ip):
  try:
    requests.get(f"http://{ip}:80", timeout=5)
    return {"IP": str(ip), "STATUS": "OK"}
  except Timeout:
    return {"IP": str(ip), "STATUS": "TIMEOUT"}

results = pd.DataFrame(thread_map(check_ip, network))
results["timestamp"] = pd.Timestamp.now()
print(results.STATUS.value_counts())
if os.path.isfile("results.csv"):
    results.to_csv("results.csv", mode="a", index=False, header=False)
else:
    results.to_csv("results.csv", mode="a", index=False, header=True)
