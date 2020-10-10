import sys
import numpy as np
import time
import SPTAGClient

print("---- Script execution started ----")

print("Number of arguments: " + str(len(sys.argv)))
print("Argument List: " + str(sys.argv))

aggregator_ip = ""
aggregator_port = ""

if len(sys.argv) < 2:
    aggregator_ip = "192.168.29.41"
else:
    aggregator_ip = sys.argv[1]

print("aggregator_ip: {}".format(aggregator_ip))

if len(sys.argv) < 3:
    aggregator_port = "8100"
else:
    aggregator_port = sys.argv[2]

print("aggregator_port: {}".format(aggregator_port))

# connect to the server
# local server ip and port: "127.0.0.1", "8000"
# local aggregator ip and port: "192.168.29.41", "8100"
# remote vm ip and port: "52.255.166.26", "8100"
client = SPTAGClient.AnnClient(aggregator_ip, aggregator_port)
while not client.IsConnected():
    print("Could not connect to aggregator/server")
    time.sleep(1)
client.SetTimeoutMilliseconds(18000)

print("Connected to aggregator/server")

k = 3
vector_dimension = 10
# prepare query vector
q = np.random.rand(vector_dimension).astype(np.float32)

# AnnClient.Search(query_vector, knn, data_type, with_metadata)
result = client.Search(q, k, 'Float', True) 

print (result[0]) # nearest k vector ids
print (result[1]) # nearest k vector distances
print (result[2]) # nearest k vector metadatas

print("---- Script execution completed ----")