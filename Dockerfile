FROM "ubuntu:bionic"
RUN apt update && \
    apt install -y bash \
                   build-essential \
                   git \
                   curl \
                   ca-certificates \
                   python3 \
                   python3-pip && \
    rm -rf /var/lib/apt/lists
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    tensorflow-cpu \
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