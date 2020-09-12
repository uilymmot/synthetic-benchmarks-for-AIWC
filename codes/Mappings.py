
#Parses raw outputs from Oclgrind kernel regions into the names used for opencl predictions with aiwc
#######################################################
kernelMappings = { 
    # dwt2d
    "c_CopySrcToComponents_kernel":"c_CopySrcToComponents", 
    "kl_fdwt53Kernel_kernel":"cl_fdwt53Kernel", 
    # csr
    "csr_kernel":"csr", 
    # lud
    "diagonal_kernel":"lud_diagonal", 
    "perimeter_kernel":"lud_perimeter", 
    "internal_kernel":"lud_internal", 
    # srad
    "srad1_kernel":"srad_cuda_1", 
    "srad2_kernel":"srad_cuda_2",
    # kmeans
    "kmeans_kernel":"kmeansPoint", 
    "kmeans_kernel":"kmeansPoint", 
    # openclfft
    "fft_kernel":"fftRadix16Kernel", 
    # bfs
    "kernel1_kernel":"kernel1", 
    "kernel2_kernel":"kernel2",
    # crc
    "kernel_compute_kernel":"crc32_slice8", 
    # bwa_hmm
    "_cl_kernel_init_ones_dev_kernel":"init_ones_dev", 
    "_cl_kernel_init_alpha_dev_kernel":"init_alpha_dev", 
    "_cl_kernel_init_beta_dev_kernel":"init_beta_dev",
    "__cl_kernel_scale_alpha_dev_kernel":"scale_alpha_dev",
    "_cl_kernel_scale_a_dev_kernel":"scale_a_dev", 
    "_cl_kernel_scale_b_dev_kernel":"scale_b_dev", 
    "__cl_kernel_s_dot_kernel_naive_kernel":"s_dot_kernel_naive", 
    "_cl_kernel_calc_alpha_dev_kernel":"calc_alpha_dev", 
    "_cl_kernel_calc_beta_dev_kernel":"calc_beta_dev", 
    "_cl_kernel_calc_gamma_dev_kernel":"calc_gamma_dev", 
    "_cl_kernel_calc_xi_dev_kernel":"calc_xi_dev", 
    "_cl_kernel_acc_b_dev_kernel":"acc_b_dev",
    "_cl_kernel_est_a_dev_kernel":"est_a_dev", 
    "_cl_kernel_est_b_dev_kernel":"est_b_dev", 
    "_cl_kernel_est_pi_dev_kernel":"est_pi_dev", 
    "_cl_kernel_sgemvn_kernel_naive_kernel":"mvm_non_kernel_naive", 
    "_cl_kernel_sgemvt_kernel_naive_kernel":"mvm_trans_kernel_naive", 
    # needle
    "clKernel_nw1_kernel":"needle_opencl_shared_1", 
    "clKernel_nw2_kernel":"needle_opencl_shared_2", 
    # swat
    "hTraceBackKernel":"trace_back2",
    "hMatchStringKernel_kernel":"MatchStringGPUSync",
    # gem
    "calc_potential_single_step_dev":"calc_potential_single_step_dev"  
    # nqueens
}
    ## missing:
    ## nqueens
    ## It appears that DW2TD is GPU only??
    # Kmeans - "Invert_mapping" no longer seems to exist
    # What are the differences between fftRadix2,4,8,16?
    
renameDictionary = {
    "application":"application",
    "size":"size",
    "opcode":"opcode",
    "granularity":"granularity",
    "barriers per instruction":"barriers_per_instruction",
    "instructions per operand":"instructions_per_operand",
    "total instruction count":"total_instruction_count",
    "workitems":"workitems",
    "operand sum":"operand_sum",
    "total # of barriers hit":"total_barriers_hit",
    "min instructions to barrier":"min_instructions_to_barrier",
    "max instructions to barrier":"max_instructions_to_barrier",
    "median instructions to barrier":"median_instructions_to_barrier",
    "max simd width":"max_simd_width",
    "mean simd width":"mean_simd_width",
    "stdev simd width":"stddev_simd_width",
    "total memory footprint":"total_memory_footprint",
    "90% memory footprint":"ninety_percent_memory_footprint",
    "global memory address entropy":"global_memory_address_entropy",
    "local memory address entropy -- 1 LSBs skipped":"local_memory_address_entropy_1",
    "local memory address entropy -- 2 LSBs skipped":"local_memory_address_entropy_2",
    "local memory address entropy -- 3 LSBs skipped":"local_memory_address_entropy_3",
    "local memory address entropy -- 4 LSBs skipped":"local_memory_address_entropy_4",
    "local memory address entropy -- 5 LSBs skipped":"local_memory_address_entropy_5",
    "local memory address entropy -- 6 LSBs skipped":"local_memory_address_entropy_6",
    "local memory address entropy -- 7 LSBs skipped":"local_memory_address_entropy_7",
    "local memory address entropy -- 8 LSBs skipped":"local_memory_address_entropy_8",
    "local memory address entropy -- 9 LSBs skipped":"local_memory_address_entropy_9",
    "local memory address entropy -- 10 LSBs skipped":"local_memory_address_entropy_10",
    "total unique branch instructions":"total_unique_branch_instructions",
    "90% branch instructions":"ninety_percent_branch_instructions",
    "branch entropy (yokota)":"branch_entropy_yokota",
    "branch entropy (average linear)":"branch_entropy_average_linear",
    "device":"device",
    "total_time":"total_time",
    "kernel_time":"kernel_time"
}
