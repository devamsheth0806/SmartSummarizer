FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip3 install -r requirements.txt

# install nltk dependencies
RUN [ "python3", "-c", "import nltk; nltk.download('all')" ]

# tell the port number the container should expose
EXPOSE 8887

# run the command
CMD ["python3", "./GUI_1.6.py"]
