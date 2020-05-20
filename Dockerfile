FROM tensorflow/tensorflow:latest-py3
RUN apt-get update && \
    apt-get install -y git
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    transformers \
    googletrans \
    git+https://github.com/devajithvs/search-engine-parser.git
WORKDIR ~/question-answering-api
RUN mkdir src
RUN cd src
RUN mkdir model
RUN ls -la
RUN python ./downloader.py
COPY . /src
CMD [ "python", "-u", "src/scraper.py" ]