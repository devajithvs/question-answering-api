FROM tensorflow/tensorflow:latest
RUN apt-get update
RUN apt-get install git -y
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir \
    transformers \
    googletrans \
    git+https://github.com/devajithvs/search-engine-parser.git
RUN mkdir src
RUN cd src
RUN mkdir model
RUN python downloader.py
COPY . /src
CMD [ "python", "-u", "src/scraper.py" ]
