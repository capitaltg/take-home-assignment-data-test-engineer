# Local PySpark environment. Mirrors AWS Glue 5.0: Python 3.11, Spark 3.5, Java 17.
FROM python:3.11-slim-bookworm

# Installs Java 17 and links it to /opt/java so JAVA_HOME works on Intel and Apple Silicon.
RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-17-jre-headless procps make \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(dirname "$(readlink -f "$(which java)")")")" /opt/java

ENV JAVA_HOME=/opt/java \
    PYTHONPATH=/app/src \
    PYSPARK_PYTHON=python \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source is bind-mounted at runtime (see Makefile / docker-compose.yml) so edits are live.
CMD ["python", "scripts/check_env.py"]
