import os
import numpy as np
from datetime import datetime
import SPTAG

print("---- Script execution started ----")

current_working_dir = os.getcwd()

print("Working directory: {}".format(current_working_dir))

if not os.path.exists(os.path.join(current_working_dir, "indexes")):
    print("indexes folder does not exist. Creating indexes folder")
    os.makedirs(os.path.join(current_working_dir, "indexes"))
    print("indexes folder created")

vector_number = 100
vector_dimension = 10

current_datetime = datetime.now()
formatted_dateTime = current_datetime.strftime("%Y%m%dT%H%M%S")

# Randomly generate the database vectors. 
# Currently SPTAG only support int8, int16 and float32 data type.
x = np.random.rand(vector_number, vector_dimension).astype(np.float32) 

# Prepare metadata for each vectors, separate them by '\n'. 
# Currently SPTAG python wrapper only support '\n' as the separator
m = ''
for i in range(vector_number):
    m += str(i) + '\n'

index = SPTAG.AnnIndex('BKT', 'Float', vector_dimension)

# Set the thread number to speed up the build procedure in parallel 
index.SetBuildParam("NumberOfThreads", '4')

# Set the distance type. Currently SPTAG only support Cosine and L2 distances. 
# Here Cosine distance is not the Cosine similarity. The smaller Cosine distance it is, the better.
index.SetBuildParam("DistCalcMethod", 'Cosine') 

if index.BuildWithMetaData(x, m, vector_number, False):
    index.Save("indexes\\sptag_index_{}".format(formatted_dateTime)) # Save the index to the disk

# os.listdir("indexes\\sptag_index_{}".format(formatted_dateTime))

# Local index test on the vector search
search_index = SPTAG.AnnIndex.Load("indexes\\sptag_index_{}".format(formatted_dateTime))

# prepare query vector
q = np.random.rand(vector_dimension).astype(np.float32)

# Search k=3 nearest vectors for query vector q
result = search_index.SearchWithMetaData(q, 3)
print (result[0]) # nearest k vector ids
print (result[1]) # nearest k vector distances
print (result[2]) # nearest k vector metadatas

print("---- Script execution completed ----")