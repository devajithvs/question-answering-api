FROM tensorflow/tensorflow:latest-py3
RUN apt-get update && \
    apt-get install -y git
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    transformers \
    googletrans \
    git+https://github.com/devajithvs/search-engine-parser.git
COPY . /home/devajith/question-answering-api
WORKDIR /home/devajith/question-answering-api
RUN mkdir test
RUN ls -la
RUN python ./downloader.py
COPY . /src
CMD [ "python", "-u", "scraper.py" ]