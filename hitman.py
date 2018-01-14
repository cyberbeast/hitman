# |*|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|*|
# |*| AUTHOR: Sandesh Gade, Gautam Somappa                  |*|
# |*| github: github.com/cyberbeast                         |*|
# |*| email: sandeshgade@gmail.com, gautam.somappa@gmail.com|*|
# |*|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|*|
# |*| ALGORITHM for script:                                 |*|
# |*| 1.    Loop through                                    |*|
# |*| 2.    ---- make request & start timer                 |*|
# |*| 3.    ---- check response status                      |*|
# |*| 4.    ---- if response status is 200                  |*|
# |*| 5.    ---- ---- stop timer, calculate elapsed time    |*|
# |*| 6.    ---- ---- push elapsed time to list             |*|
# |*| 7.    ---- else print appropriate message             |*|
# |*| 8.    Calculate min, max and average latency.         |*|
# |*| 9.    plot a graph and export graph as image.         |*|
# |*|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|*|
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
import sys
import requests
from requests.exceptions import HTTPError
import time
import matplotlib
import argparse
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# init vars
class Latency:
    cur_hits = 0
    total_latency_list = []
    round_trip_without_data_list = []
    round_trip_time_data_only_list = []
    def __init__(self,url,max_hits,time_between_hits=0,verbose=False):
        self.max_hits = max_hits
        while(self.cur_hits < self.max_hits):
            try:
                start = time.time()
                protocol = url.strip("https://")
                url="http://"+protocol
                r = requests.get(url)
                r.raise_for_status()
                end = time.time()
                self.cur_hits += 1 #increment cur_hit counter
                round_trip = end - start
                round_trip_without_data = r.elapsed.total_seconds()
                if verbose:
                    print("HIT " + str(self.cur_hits) + "\t: STATUS " + str(r.status_code) + "\t: TOTAL " + str(round_trip) + "\t: INIT+HEADERS " + str(r.elapsed.total_seconds()) + "\t: DATA " + str(round_trip - round_trip_without_data))
                self.total_latency_list.append(round_trip)
                self.round_trip_without_data_list.append(r.elapsed.total_seconds())
                self.round_trip_time_data_only_list.append(round_trip - round_trip_without_data)
                time.sleep(time_between_hits)
            except HTTPError:
                print("HTTPError -- " + str(r.status_code))
                print("Exiting...")
                sys.exit()

        print("Testing complete. Calculating results...")
        print("MAX \t " + str(max(self.total_latency_list)))
        print("MIN \t " + str(min(self.total_latency_list)))
        print("AVG \t " + str(sum(self.total_latency_list)/len(self.total_latency_list)))

    def generate_graph(self,file_prefix):
        print("Generating graphs...")
        ind = [x for x in range(self.max_hits)]
        p1 = plt.bar(ind, self.round_trip_without_data_list, color='#d62728')
        p2 = plt.bar(ind, self.round_trip_time_data_only_list, bottom=self.round_trip_without_data_list)
        plt.ylabel('Latency (s)')
        plt.xlabel('HIT')
        plt.legend((p1[0], p2[0]), ('INIT+HEADERS', 'DATA'))
        print("Saving graph as " + '"' + file_prefix + " " + time.strftime("%c") + '.png"')
        plt.savefig(file_prefix + " " + time.strftime("%c"))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Hitman is a python environment that makes requests to a given url and measures min, max and average end-to-end latency.')
    parser.add_argument('--url', type=str, help='Enter url', required=True)
    parser.add_argument('--max_hits', type=int, help='Enter max hits', required=True)
    parser.add_argument('--time', type=int, help='Enter time between hits', required=False)
    parser.add_argument('--file', type=str, help='Enter file to be saved in', required=False)
    parser.add_argument('--verbose', help='Use this to show full results', required=False, action="store_true")
    parser.add_argument('--graph', help='Generate graph', required=False, action="store_true")
    args = parser.parse_args()
    url = args.url
    max_hits = args.max_hits
    if args.time is not None:
        time_between_hits = args.time
    file_prefix = args.file
    latency = Latency(url,max_hits)
    if file_prefix and args.graph:
        latency.generate_graph(file_prefix)
