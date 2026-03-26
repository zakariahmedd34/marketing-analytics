FROM python:3.11-slim

RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas numpy matplotlib seaborn scikit-learn scipy requests openpyxl

RUN mkdir -p /app/pipeline/

COPY . /app/pipeline/

WORKDIR /app/pipeline/

CMD ["/bin/bash"]