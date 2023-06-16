FROM python:3.10

ENV LANG C.UTF-8

RUN apt-get update;

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir /scripts

ADD Django_Bike_Res/requirements.txt /app/requirements.txt
ADD entrypoint.sh /scripts/entrypoint.sh

WORKDIR /app

RUN chmod +x ../scripts/*.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install nano
RUN apt-get -y install nano
# Install cron
RUN apt-get -y install cron
# Add the cron job
RUN crontab -l | { cat; echo "* * * * * python /app/manage.py getlocation"; } | crontab -
RUN crontab -l | { cat; echo "* * * * * python /app/manage.py getstatus"; } | crontab -

ADD Bike_Res /app
# COPY . /app

# Run the command on container startup
CMD cron
