cd /phd
# list the available OpenCL devices

# runs the basic synthesizer
bazel run //deeplearning/clgen -- --config /workspace/codes/synthetic-benchmark-driver/tiny_synthesizer_config.pbtxt
# list the directory where the synthesizer outputs
bazel run //deeplearning/clgen -- --print_cache_path=sampler --config /workspace/codes/synthetic-benchmark-driver/tiny_synthesizer_config.pbtxt 

# to get the directory where all the kernels were generated:
//deeplearning/clgen -- --config /workspace/codes/tiny_synthesizer_config.pbtxt --print_cache_path=sampler > .synthesized_kernel_directory ; export SYNTHESIZED_KERNEL_DIRECTORY=$(cat .synthesized_kernel_directory)

cd /workspace/codes/synthetic-benchmark-driver/
# run these synthesized kernels on the synthetic benchmark driver tool
./sbd_over_directory.sh $SYNTHESIZED_KERNEL_DIRECTORY tiny 0 0 runtime

