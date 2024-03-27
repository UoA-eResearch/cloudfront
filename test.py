#!/usr/bin/env python3

from netaddr import IPNetwork
import requests
from requests.exceptions import ConnectTimeout
from tqdm.auto import tqdm
from tqdm.contrib.concurrent import thread_map
import pandas as pd

network = list(IPNetwork("65.9.141.27/24"))
print(f"Scanning {network[0]} to {network[-1]}")

def check_ip(ip):
  try:
    requests.get(f"http://{ip}:80", timeout=(3.05, 27)) # connect, read
    return {"IP": str(ip), "STATUS": "OK"}
  except ConnectTimeout:
    return {"IP": str(ip), "STATUS": "TIMEOUT"}

results = pd.DataFrame(thread_map(check_ip, network))
results["timestamp"] = pd.Timestamp.now()
print(results.STATUS.value_counts())
results.to_csv("results.csv", mode="a", index=False, header=False)