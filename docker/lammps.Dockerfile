FROM ubuntu:22.04
LABEL maintainer="your_name_or_project_email"
RUN apt-get update && \
    apt-get install -y lammps bc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY ./benchmarks/lammps .
RUN chmod +x run.sh
CMD ["/bin/bash", "run.sh"]
