
Inproving OpenCL Performance Prediction using Synthesized Benchmarks for the AIWC Predictive Model
---------------------------------------------------------------------------

## Installation

This project uses Docker to facilitate reproducibility. As such, it has the following dependencies:

* Cuda 9.0 Runtime -- available [here](https://developer.nvidia.com/cuda-downloads)
* Docker -- available [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* nvidia-docker2, install instructions found [here](https://github.com/NVIDIA/nvidia-docker)
* Docker nvidia container, installed with: `sudo apt install nvidia-container-runtime`
* LLVM Version 5.0 dependency for oclgrind (https://github.com/ANU-HPC/Oclgrind)
* OpenCL Predictions with AIWC (predictions folder) (https://github.com/BeauJoh/opencl-predictions-with-aiwc)

# Build

To generate a docker image named synthesizing, run:

`docker build -t username/synthesizing .`

# Run

To start the docker image run:

`docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=1 -it --mount src=`pwd`,target=/workspace,type=bind -p 8888:8888 --net=host username/synthesizing`

Note the `NVIDIA_VISIBLE_DEVICES` variable is the requested device id, which allows individual container instances to access one device - this is not required unless generation of kernels using the included CLgen (Cuda) model is desired.

## CLgen from model

From docker navigate to the '/workspace/codes/paper-synthesizing-benchmarks-model' directory

To run the model run the command 'python resurrect-paper-model.py'

To run the model to generate kernels and their aiwc features spaces navigate to '/workspace/codes'

run the command 'python make-kernels-and-features.py'

This will deposit kernels into the directory '/workspace/codes/generatedkernels'
Along with corresponding AIWC feature spaces into '/wordspace/codes/generatedkernelfeatures'

# Workbook code Using Synthetic Kernels to Improve OpenCL Prediction Performance

Code samples can be found in '/workspace/codes/synthesize-and-run-kernels.ipynb'

To run this notebook, navigate to '/workspace/codes' directory and run beakerx using the instructions in the below section.

This notebook contains codes to generate and sample kernels. These kernels are saved to generatedKernels, their feature spaces are saved to generatedkernelfeatures. 
Running the codes in the notebook multiple times will overwrite each generatedkernel and generatedkernelfeatures directory. 

An example set of generated kernels can be found in 'workspace/codes/generatedkernelbatch1'

# Workbook Examples

For reproducibility, BeakerX has also been added for replicating results and for the transparency of analysis.
It is lauched by running:

`cd codes`
`beakerx --allow-root`

from within the container and following the prompts to access it from the website front-end.

*Note* that if this node is accessed from an ssh session local ssh port forwarding is required and is achieved with the following:

`ssh -N -f -L localhost:8888:localhost:8888 <node-name>`

A notebook including codes for analysing the data generated from this artefact is included in codes/predictions/Synthetic Benchmark Analysis.ipynb.

A notebook containing codes for generation and analysis of CLgen kernels can be found in codes/Kernel Generation Using CLgen.ipynb.



