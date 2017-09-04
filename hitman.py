# Loop through
# ---- make request & start timer
# ---- check response status
# ---- if response status is 200
# ---- ---- stop timer, calculate elapsed time
# ---- ---- push elapsed time to list
# ---- else print appropriate message

# Calculate min, max and average latency.

# ~~~~~FUTURE: plot a graph.

import sys
import requests
from requests.exceptions import HTTPError
from timeit import default_timer as timer

# read params
url = input('Enter url: \t')
max_hits = int(input('Enter max_hits: \t'))

# init vars
cur_hits = 0
latency_list = []

while(cur_hits < max_hits):
    r = requests.get(url)
    start = timer()

    try:
        r.raise_for_status()
    except HTTPError:
        print("HTTPError -- " + str(r.status_code))
        print("Exiting...")
        sys.exit()

    end = timer()
    cur_hits += 1
    print("HIT " + str(cur_hits) + "\t:\t" + str(r.status_code) + "\t" + str(end - start))
    latency_list.append(end-start)
 
print("Testing complete. Calculating results...")
print("MAX \t " + str(max(latency_list)))
print("MIN \t " + str(min(latency_list)))
print("AVG \t " + str(sum(latency_list)/len(latency_list)))