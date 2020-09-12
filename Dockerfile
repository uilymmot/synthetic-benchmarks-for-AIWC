# An Ubuntu environment configured for building papers written in pandoc
FROM nvidia/opencl:devel-ubuntu16.04

MAINTAINER Beau Johnston <beau.johnston@anu.edu.au>

# Disable post-install interactive configuration.
# For example, the package tzdata runs a post-installation prompt to select the
# timezone.
ENV DEBIAN_FRONTEND noninteractive
#

# use the closest Ubuntu mirror
RUN echo "deb mirror://mirrors.ubuntu.com/mirrors.txt xenial main restricted universe multiverse" > /etc/apt/sources.list \
 && echo "deb mirror://mirrors.ubuntu.com/mirrors.txt xenial-updates main restricted universe multiverse" >> /etc/apt/sources.list \
 && echo "deb mirror://mirrors.ubuntu.com/mirrors.txt xenial-security main restricted universe multiverse" >> /etc/apt/sources.list \
 && apt-get update

# Setup the environment.
ENV HOME /root
ENV USER docker

# Install essential packages.
RUN apt-get update && apt-get install --no-install-recommends -y \
    apt-transport-https \
    build-essential \
    git \
    less \
    make \
    pkg-config \
    software-properties-common \
    vim \
    wget \
    zlib1g-dev 

   
# Install R and model dependencies
#RUN apt-get update && apt-get install --no-install-recommends -y dirmngr
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
#RUN add-apt-repository ppa:marutter/rrutter && apt-get -y --no-install-recommends update && apt-get -y upgrade
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/' && apt-get update && apt-get -y upgrade
RUN apt-get update && apt-get install -y --no-install-recommends \
    r-base-core \
    r-base-dev \
    r-recommended
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev
RUN Rscript -e "install.packages('devtools')" \
    && Rscript -e "devtools::install_github('imbs-hl/ranger')" \
    && Rscript -e "devtools::install_github('cran/RJSONIO')"\
    && Rscript -e "devtools::install_github('r-lib/httr')" \
    && Rscript -e "install.packages('tidyverse')" \
    && Rscript -e "devtools::install_github('BeauJoh/fmsb')" \
    && Rscript -e "devtools::install_url('https://github.com/wilkelab/cowplot/archive/0.6.3.zip')" \
    && Rscript -e "devtools::install_url('https://github.com/cran/gridGraphics/archive/0.3-0.zip')" \
    && Rscript -e "devtools::install_github('cran/Metrics')" \
    && Rscript -e "devtools::install_github('cran/latex2exp')" \
    && Rscript -e "devtools::install_github('cran/akima')" \
    && Rscript -e "devtools::install_github('cran/pander')"

#Install CUDA 9.0 (for this version of Tensorflow)
# Add NVIDIA package repository
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
RUN wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
RUN rm -rf /etc/apt/sources.list.d/cuda.list
RUN apt-get update && apt-get install --no-install-recommends -y ./cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
RUN wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb
RUN apt-get install ./nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb

# Install CUDA and tools. Include optional NCCL 2.x
RUN apt-get update && apt-get install --no-install-recommends -y --allow-downgrades --allow-change-held-packages \
    cuda9.0 \
    cuda-command-line-tools-9-0 \
    cuda-cublas-9-0 \
    cuda-cufft-9-0 \
    cuda-curand-9-0 \
    cuda-cusolver-9-0 \
    cuda-cusparse-9-0 \
    cuda-toolkit-9-0 \
    libcudnn7=7.2.1.38-1+cuda9.0 \
    libcudnn7-dev=7.2.1.38-1+cuda9.0 \
    libnccl2=2.2.13-1+cuda9.0 
RUN ln -s /usr/local/cuda-9.0 /usr/local/cuda && \
    ln -s /usr/lib/x86_64-linux-gnu/libcuda.so /usr/local/cuda/lib64/libcuda.so &&\
    ln -s /usr/lib/x86_64-linux-gnu/libcudnn.so /usr/local/cuda/lib64/libcudnn.so &&\
    ldconfig

# Install OpenCL Device Query tool
RUN git clone https://github.com/BeauJoh/opencl_device_query.git /opencl_device_query
WORKDIR /opencl_device_query
RUN make

# Install Intel CPU Runtime for OpenCL Applications 18.1 for Linux (OpenCL 1.2)
RUN apt-get update && apt-get install -qqy \
    lsb-core \
    libnuma1 \
 && export RUNTIME_URL="http://registrationcenter-download.intel.com/akdlm/irc_nas/vcp/15532/l_opencl_p_18.1.0.015.tgz" \
    && export TAR=$(basename ${RUNTIME_URL}) \
    && export DIR=$(basename ${RUNTIME_URL} .tgz) \
    && wget -q ${RUNTIME_URL} \
    && tar -xf ${TAR} \
    && sed -i 's/decline/accept/g' ${DIR}/silent.cfg \
    && ${DIR}/install.sh --silent ${DIR}/silent.cfg \
;fi


# Install the OpenCL Nvidia drivers
RUN echo /usr/lib/x86_64-linux-gnu/libnvidia-opencl.so.1 > /etc/OpenCL/vendors/nvidia.icd

# Install the OpenCL c++ headers
RUN apt-get update && apt-get install -qqy opencl-headers

# Install LibSciBench
ENV LSB_SRC /libscibench-source
ENV LSB /libscibench
RUN apt-get update && apt-get install --no-install-recommends -y \
    cmake \
    clang-5.0 \
    gcc \
    g++ \
    llvm-5.0 \
    llvm-5.0-dev \
    libclang-5.0-dev

RUN git clone https://github.com/spcl/liblsb.git $LSB_SRC
WORKDIR $LSB_SRC
RUN ./configure --without-mpi --without-papi --prefix=$LSB && make && make install

# Install beakerx
#RUN deb http://mirrors.kernel.org/ubuntu xenial-updates main 
RUN apt-get update && apt-get install --no-install-recommends -y python3-pip python3-setuptools python3-dev libreadline-dev libpcre3-dev libbz2-dev liblzma-dev --fix-missing
RUN pip3 install --upgrade pip
RUN pip3 install tzlocal ipywidgets pandas py4j==0.10.9 requests beakerx-tabledisplay beakerx \
    && beakerx install
RUN pip3 install rpy2==3.0.5
#RUN pip3 install torch===1.2.0 torchvision===0.4.0 -f https://download.pytorch.org/whl/torch_stable.html

# Install R module for beakerx
RUN Rscript -e "devtools::install_github('IRkernel/IRkernel')"\
    && Rscript -e "IRkernel::installspec(user = FALSE)"\
    && Rscript -e "devtools::install_github('cran/RJSONIO')"\
    && Rscript -e "devtools::install_github('r-lib/httr')"\
    && Rscript -e "devtools::install_github('tidyverse/magrittr')"\
    && Rscript -e "devtools::install_github('tidyverse/ggplot2')"\
    && Rscript -e "devtools::install_github('tidyverse/tidyr')"\
    && Rscript -e "devtools::install_github('BeauJoh/fmsb')"\
    && Rscript -e "devtools::install_github('wilkelab/cowplot')"\
    && Rscript -e "devtools::install_github('cran/gridGraphics')"\
    && Rscript -e "devtools::install_github('cran/Metrics')"\
    && Rscript -e "devtools::install_github('cran/latex2exp')"\
    && Rscript -e "devtools::install_github('cran/akima')" \
    && Rscript -e "devtools::install_github('cran/pander')"
RUN beakerx install

# Install LetMeKnow
RUN pip3 install -U 'lmk==0.0.14'
# setup lmk by copying or add .lmkrc to /root/
# is used as: python3 ../opendwarf_grinder.py 2>&1 | lmk -
# or: lmk 'python3 ../opendwarf_grinder.py'

#########################################################################################
# Dependencies for Benchmarking, Analysing and Modelling with Random Forest Predictors. #
#########################################################################################

# Install the Extended OpenDwarfs (EOD) Benchmark Suite
ENV EOD /OpenDwarfs
RUN apt-get update && apt-get install --no-install-recommends -y autoconf libtool automake
RUN git clone https://github.com/BeauJoh/OpenDwarfs.git $EOD
WORKDIR $EOD
RUN ./autogen.sh
RUN mkdir build
WORKDIR $EOD/build
RUN ../configure --with-libscibench=$LSB
RUN make

RUN cmake --version


# Install OclGrind
#ENV OCLGRIND_SRC /oclgrind-source
#ENV OCLGRIND /oclgrind
#ENV OCLGRIND_BIN /oclgrind/bin/oclgrind
#RUN git clone https://github.com/BeauJoh/Oclgrind.git $OCLGRIND_SRC
#WORKDIR $OCLGRIND_SRC/build
#ENV CC clang-5.0
#ENV CXX clang++-5.0
#RUN cmake $OCLGRIND_SRC -DUSE_LEVELDB=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLLVM_DIR=/usr/lib/llvm5.0/lib/cmake -DCLANG_ROOT=/usr/lib/clang/5.0 -DCMAKE_INSTALL_PREFIX=$OCLGRIND \
#    && make \
#    && make install

# Install Random Forest Predictor
ENV PREDICTIONS /opencl-predictions-with-aiwc
RUN git clone https://github.com/BeauJoh/opencl-predictions-with-aiwc.git $PREDICTIONS

#Install CUDA 8.0 (Torch -- for the artefact of clgen)
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
RUN wget https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
RUN rm -rf /etc/apt/sources.list.d/cuda.list
RUN dpkg -i  ./cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
RUN apt-get update && apt-get install --no-install-recommends -y --allow-downgrades --allow-change-held-packages \
    cuda8.0 \
    cuda-cublas-8-0 \
    cuda-cufft-8-0 \
    cuda-curand-8-0 \
    cuda-command-line-tools-8-0 \
    cuda-toolkit-8-0
RUN rm -f /usr/local/cuda /usr/local/cuda/lib64/libcuda.so /usr/local/cuda/lib64/libcudnn.so
RUN ln -s /usr/local/cuda-8.0 /usr/local/cuda && \
    ln -s /usr/lib/x86_64-linux-gnu/libcuda.so /usr/local/cuda/lib64/libcuda.so &&\
    ln -s /usr/lib/x86_64-linux-gnu/libcudnn.so /usr/local/cuda/lib64/libcudnn.so &&\
    ldconfig

# Install old version of clgen for the scaper tool
RUN add-apt-repository ppa:deadsnakes/ppa\
    && apt-get update && apt-get install -yyq \
    curl \
    gcc \
    g++ \
    libomp-dev \
    python3.6 \
    sudo \
    virtualenv
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1 \
    && update-alternatives  --set python /usr/bin/python3.6 \
    && mkdir -p /usr/lib/python3.6/site-packages/
WORKDIR /
RUN git clone https://github.com/ChrisCummins/clgen.git /scrape-clgen
WORKDIR /scrape-clgen
RUN git checkout tags/0.1.7 \
    && curl -s https://raw.githubusercontent.com/ChrisCummins/clgen/0.1.7/install-deps.sh | bash
# Use a virtual environment --  as-per the old CLgen way
ENV VIRTUAL_ENV=/clgen-venv
RUN python3 -m virtualenv --python=/usr/bin/python3.6 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN update-alternatives --set cc /usr/bin/gcc && update-alternatives --set c++ /usr/bin/g++
RUN apt-get update && apt-get install -yyq \
    python-dev \
    python3.6-dev \
    libhdf5-serial-dev
RUN pip3 install rpy2
RUN pip3 install --no-cache-dir h5py python-dateutil==2.6.1 pytz==2017.2
RUN CC="gcc" CXX="g++" ./configure --batch --with-cuda --with-dev-tools
COPY ./codes/paper-synthesizing-benchmarks-model/libclc.make make/libclc.make
COPY ./codes/paper-synthesizing-benchmarks-model/clgen-fixed-makefile ./Makefile
RUN CC="gcc" CXX="g++" make
RUN PIP=/clgen-venv/bin/pip3 PYTHON=/clgen-venv/bin/python3 HDF5_DIR=/usr/lib/x86_64-linux-gnu/hdf5/serial make install

#install locales
RUN apt-get update && apt-get install -yqq \
    language-pack-en-base \
    && dpkg-reconfigure locales
RUN /clgen-venv/bin/pip3 install ipython

RUN pip3 install numpy==1.16.4
# Beakerx (Jupyter)
RUN /clgen-venv/bin/pip3 install ipywidgets pandas py4j requests matplotlib beakerx \
    && beakerx install

#container variables and startup...
ENV LD_LIBRARY_PATH "${LSB}/lib:${LD_LIBRARYPATH}"
ENV CPATH "${LSB}/include:${CPATH}"
WORKDIR /workspace

RUN echo 'alias ipython=/clgen-venv/bin/ipython3; alias python3=/clgen-venv/bin/python3; alias pip=/clgen-venv/bin/pip3' >> ~/.bashrc

CMD /bin/bash
