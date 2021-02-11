FROM python:3.6

# alias in case of interact with container
RUN echo 'alias ll="ls -althF --color=auto"' >> ~/.bashrc

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir $HOME
RUN mkdir $APP_HOME

WORKDIR $APP_HOME

# We copy just the requirements.txt first to leverage Docker cache
COPY ["./requirements.txt", "."]

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY [".", "$APP_HOME/"]
