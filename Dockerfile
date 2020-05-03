FROM tensorflow/tensorflow:latest
RUN apt-get update
RUN apt-get install git -y
RUN python -m pip install --upgrade pip 
RUN python -m pip install --no-cache-dir \
    transformers \
    googletrans
    # git+https://github.com/devajithvs/search-engine-parser.git
WORKDIR ~/docker/question-answering-api
RUN mkdir src
RUN cd src
RUN mkdir model
RUN ls -la
RUN python downloader.py
COPY . /src
CMD [ "python", "-u", "src/scraper.py" ]
