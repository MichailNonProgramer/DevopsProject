FROM ubuntu:22.04
LABEL maintainer="your_name_or_project_email"
RUN apt-get update && \
    apt-get install -y python3 python3-pip bc && \
    pip3 install --no-cache-dir espresso && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY ./benchmarks/espresso .
RUN chmod +x run.sh
CMD ["/bin/bash", "run.sh"]
