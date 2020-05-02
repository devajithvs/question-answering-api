FROM python:3
RUN pip install transformers
RUN pip install tensorflow
RUN pip install googletrans
RUN pip install 'git+https://github.com/devajithvs/search-engine-parser.git'
RUN mkdir src
RUN cd src
RUN mkdir model
COPY . /src
CMD [ "python", "-u", "src/scraper.py" ]