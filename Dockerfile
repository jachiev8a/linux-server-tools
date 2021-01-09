FROM python:3.6

WORKDIR /app

# We copy just the requirements.txt first to leverage Docker cache
COPY ["./requirements.txt", "/app/requirements.txt"]

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY [".", "/app/"]

# run server to be seen from outside
# ----------------------------------------------------------------------
CMD ["flask", "run", "--host=0.0.0.0"]
