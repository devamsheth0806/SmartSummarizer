FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN apt-get -y update
RUN apt-get -y install xauth
RUN apt-get -y install vim
RUN pip3 install -r requirements.txt
RUN [ "python3", "-c", "import nltk; nltk.download('all')" ]

# tell the port number the container should expose
EXPOSE 8887

# run the command
CMD ["python3", "./GUI_1.8.py"]
