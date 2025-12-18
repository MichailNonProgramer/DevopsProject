FROM ubuntu:22.04
LABEL maintainer="your_name_or_project_email"
RUN apt-get update && \
    apt-get install -y gromacs bc time python3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY ./config/common.json ./config/common.json
COPY ./benchmarks/gromacs .
RUN chmod +x run.sh
CMD ["/bin/bash", "run.sh"]
