FROM maven:3.9.16-eclipse-temurin-17 AS dependency-resolver

WORKDIR /build
COPY spark/runtime/pom.xml /build/pom.xml
RUN mvn -B -q -f /build/pom.xml dependency:copy-dependencies \
      -DincludeScope=runtime \
      -DoutputDirectory=/deps

FROM apache/spark:4.0.4-scala2.13-java17-python3-r-ubuntu

USER root
ENV PIP_DEFAULT_TIMEOUT=120 PIP_RETRIES=10
RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential \
      graphviz \
      libgraphviz-dev \
      libpq-dev \
      pkg-config \
      python3-cairo \
      python3-dev; \
    rm -rf /var/lib/apt/lists/*

COPY spark/runtime/requirements-ml.txt /tmp/requirements-ml.txt
COPY spark/runtime/requirements-jupyter.txt /tmp/requirements-jupyter.txt
RUN set -eux; \
    python3 -m pip install --no-cache-dir -r /tmp/requirements-ml.txt; \
    python3 -m pip install --no-cache-dir -r /tmp/requirements-jupyter.txt; \
    python3 -m pip check; \
    rm -f /tmp/requirements-ml.txt /tmp/requirements-jupyter.txt

COPY --from=dependency-resolver /deps/ /opt/spark/jars/

RUN set -eux; \
    mkdir -p /home/spark/.config /home/spark/.cache /home/spark/.jupyter \
      /home/spark/.local/share/jupyter/runtime /opt/spark/notebooks \
      /opt/spark/events /opt/spark/warehouse /tmp/spark-ivy; \
    chown -R spark:spark /home/spark /opt/spark/notebooks \
      /opt/spark/events /opt/spark/warehouse /tmp/spark-ivy

ENV HOME=/home/spark \
    XDG_CONFIG_HOME=/home/spark/.config \
    XDG_CACHE_HOME=/home/spark/.cache \
    XDG_DATA_HOME=/home/spark/.local/share \
    JUPYTER_CONFIG_DIR=/home/spark/.jupyter \
    JUPYTER_DATA_DIR=/home/spark/.local/share/jupyter \
    JUPYTER_RUNTIME_DIR=/home/spark/.local/share/jupyter/runtime \
    PYTHONPATH=/opt/spark/python:/opt/spark/python/lib/py4j-src.zip

WORKDIR /opt/spark/notebooks
USER spark
