# hitman
Hitman is a python environment that makes requests to a given url and measures min, max and average end-to-end latency.

## Requires
* requests
* matplotlib
* argparse

## Usage
```sh
usage: hitman.py [-h] --url URL --max_hits MAX_HITS [--time TIME]
                 [--file FILE] [--verbose] [--graph]

optional arguments:
  -h, --help           show this help message and exit
  --url URL            Enter url
  --max_hits MAX_HITS  Enter max hits
  --time TIME          Enter time between hits
  --file FILE          Enter file to be saved in
  --verbose            Use this to show full results
  --graph              Generate graph

```
This is a work in progress
