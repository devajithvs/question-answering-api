FROM python:3.8-slim-buster
RUN pip install cdqa
RUN pip install googletrans
RUN pip install 'git+https://github.com/devajithvs/search-engine-parser.git'

WORKDIR ~/docker/question-answering-api
RUN mkdir src
RUN cd src
RUN mkdir model
RUN ls -la
RUN python ./downloader.py
COPY . /src
CMD [ "python", "-u", "src/scraper.py" ]
