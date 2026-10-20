FROM maven:3.9.16-eclipse-temurin-17 AS dependency-resolver

WORKDIR /build
COPY spark/runtime/pom.xml /build/pom.xml
RUN mvn -B -q -f /build/pom.xml dependency:copy-dependencies \
      -DincludeScope=runtime \
      -DoutputDirectory=/deps

FROM apache/spark:4.0.4-scala2.13-java17-python3-r-ubuntu

USER root
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
    rm -rf /var/lib/apt/lists/*; \
    python3 -m pip install --no-cache-dir -r /tmp/requirements-ml.txt; \
    python3 -m pip install --no-cache-dir -r /tmp/requirements-jupyter.txt

COPY spark/runtime/requirements-ml.txt /tmp/requirements-ml.txt
COPY spark/runtime/requirements-jupyter.txt /tmp/requirements-jupyter.txt
