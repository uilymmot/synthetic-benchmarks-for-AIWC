#!/usr/bin/env python3

import clgen.clutil
import clgen.model

version = clgen.version()
print("Successfully loaded CLgen version {}".format(version))

clgen.clutil.platform_info()

model = clgen.model.from_tar("./model.tar.bz2")

import clgen.sampler
import clgen.dbutil
import clgen.explore

argspec = ['__global float*', '__global float*', '__global float*', 'const int']
sampler = clgen.sampler.from_json({
        "kernels": { 
            "args": argspec,
            "max_length": 1000
        },
        "sampler": {
            "batch_size": 25,
            "max_kernels": 10
        }
    })

print("Seed text:", clgen.sampler.serialize_argspec(argspec), "\n")
sampler.cache(model).empty()
sampler.sample(model)

db = sampler.cache(model)["kernels.db"]
num_good_kernels = clgen.dbutil.num_good_kernels(db)
clgen.explore.explore(db)


