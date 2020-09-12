#!/usr/bin/env python3

import clgen.clutil
import clgen.model
import sqlite3
import clgen.sampler
import clgen.dbutil
import clgen.explore
import os
from subprocess import Popen, PIPE

version = clgen.version()
print("Successfully loaded CLgen version {}".format(version))

clgen.clutil.platform_info()

model = clgen.model.from_tar("./paper-synthesizing-benchmarks-model/model.tar.bz2")

argspec = ['__global float*', '__global float*', '__global float*', 'const int']
sampler = clgen.sampler.from_json({
        "kernels": { 
            "args": argspec,
            "max_length": 1000
        },
        "sampler": {
            "batch_size": 100,
            "max_kernels": 15
        }
    })

print("Seed text:", clgen.sampler.serialize_argspec(argspec), "\n")
sampler.cache(model).empty()
sampler.sample(model)

db = sampler.cache(model)["kernels.db"]
num_good_kernels = clgen.dbutil.num_good_kernels(db)
clgen.explore.explore(db)

conn = sqlite3.connect(db)
print(conn)
c = conn.cursor()

#c.execute("SELECT * FROM sqlite_master;")
c.execute("SELECT * FROM PreprocessedFiles WHERE status=0;")
rows = c.fetchall()

if not(os.path.isdir("generatedkernels")):
    os.mkdir("./generatedkernels")

for row in rows:
    name = "./generatedkernels/" + str(row[0]) + ".cl"
    newf = open(name, "w+")
    newf.writelines(row[2])
    newf.close()
    
import glob
from subprocess import Popen, PIPE

usable_kernels = []
unusable_kernels = []

if not(os.path.isdir("generatedkernelfeatures")):
    os.mkdir("./generatedkernelfeatures")
os.chdir("generatedkernelfeatures")

print("Checking next kernel batch...")
synthetic_kernel_batch = glob.glob("../generatedkernels/*.cl")
for synthetic_kernel in synthetic_kernel_batch:
    process = Popen(["../synthetic-benchmark-driver/sbc", synthetic_kernel, "tiny", "0", "0"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code == 0: #a usable kernel added it to the list to test for prediction
        usable_kernels.append(synthetic_kernel)
    else:
        unusable_kernels.append(synthetic_kernel)
print("Passed {} and failed {} kernels.".format(len(usable_kernels),len(unusable_kernels)))

print("Generating payload AIWC metrics...")
for kernel in usable_kernels:
    #TODO: add for loop for every problem size
    process = Popen(["../../../oclgrind/bin/oclgrind", "--workload-characterisation", "../synthetic-benchmark-driver/sbd", kernel, "tiny", "0", "0", "aiwc"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code == 0:
        print(output)
    
print("Querying model...")

print("Generating payload runtimes...")