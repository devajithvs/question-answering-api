FROM python:3
RUN pip install tensorflow-cpu \
    transformers \
    torch \
    googletrans \
    git+https://github.com/devajithvs/search-engine-parser.git
RUN mkdir src
RUN cd src
RUN mkdir model
RUN python downloader.py
COPY . /src
CMD [ "python", "-u", "src/scraper.py" ]
