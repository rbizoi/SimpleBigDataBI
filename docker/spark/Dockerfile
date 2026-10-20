FROM apache/spark:4.0.4-scala2.13-java17-python3-r-ubuntu

USER root

RUN python3 -m pip install --no-cache-dir jupyterlab pandas "psycopg[binary]"

RUN mkdir -p /workspace/notebooks /workspace/jobs \
    && chown -R spark:spark /workspace

ENV PYTHONPATH=/opt/spark/python:/opt/spark/python/lib/py4j-src.zip
WORKDIR /workspace
USER spark
