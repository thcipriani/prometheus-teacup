# TODO: This may need to be modified depending on your host
FROM debian:bullseye

ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        -o Dpkg::Options::="--force-confdef" \
        -o Dpkg::Options::="--force-confold" \
            "python3" \
            "python3-bpfcc" \
            "python3-iptables" \
            "python3-pip" \
            "python3-prometheus-client" \
        && rm -rf /var/lib/apt/lists/* && \
        update-alternatives --install /usr/bin/python python /usr/bin/python3 99

WORKDIR /src
COPY . .

RUN /usr/bin/python -m pip install --upgrade pip && \
    /usr/bin/python -m pip install -e .

ENV PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH
ENTRYPOINT ["teacup"]
