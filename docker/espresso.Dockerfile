FROM ubuntu:24.04
LABEL maintainer="your_name_or_project_email"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget git build-essential bc time tzdata python3 python3-dev python3-numpy python3-pip cmake gcc g++ unzip libfftw3-dev libopenmpi-dev libboost-dev libboost-mpi-dev libboost-serialization-dev libboost-test-dev && \
    ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN python3 -m pip install --no-cache-dir --break-system-packages 'Cython>=3.0.4,<3.2.0'

RUN git config --global http.postBuffer 524288000 && \
    git config --global http.lowSpeedLimit 1000 && \
    git config --global http.lowSpeedTime 60 && \
    git clone --depth 1 https://github.com/espressomd/espresso.git /opt/espresso
RUN cd /opt/espresso && mkdir build && cd build && \
    cmake .. -DWITH_PYTHON=ON && \
    make && \
    make install

RUN apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY ./config/common.json ./config/common.json
COPY ./benchmarks/espresso .
RUN chmod +x run.sh
CMD ["/bin/bash", "run.sh"]
