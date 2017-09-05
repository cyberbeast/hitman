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
import time

# read params
url = input('Enter url: \t')
max_hits = int(input('Enter max_hits: \t'))
time_between_hits = int(input('Enter time between hits: \t'))

# init vars
cur_hits = 0
latency_list = []

while(cur_hits < max_hits):
    try:
        start = time.time()
        r = requests.get(url)
        r.raise_for_status()
        end = time.time()
        cur_hits += 1 #increment cur_hit counter
        round_trip = end - start
        round_trip_without_data = r.elapsed.total_seconds()

        print("HIT " + str(cur_hits) + "\t: STATUS " + str(r.status_code) + "\t: TOTAL " + str(round_trip) + "\t: INIT+HEADERS " + str(r.elapsed.total_seconds()) + "\t: DATA " + str(round_trip - round_trip_without_data))
        latency_list.append(end-start)
        time.sleep(time_between_hits)
    except HTTPError:
        print("HTTPError -- " + str(r.status_code))
        print("Exiting...")
        sys.exit()

print("Testing complete. Calculating results...")
print("MAX \t " + str(max(latency_list)))
print("MIN \t " + str(min(latency_list)))
print("AVG \t " + str(sum(latency_list)/len(latency_list)))