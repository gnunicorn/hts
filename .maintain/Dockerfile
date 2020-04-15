# Use an official Python runtime as a parent image
FROM python:3.7

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV production

RUN mkdir /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /code/
COPY .maintain/96docker-entrypoint.sh /code/
COPY manage.py /code/
COPY hts /code/hts
# Set the working directory to /code/
WORKDIR /code/

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000

VOLUME ["/code/hts/media/", "/code/hts/static/"]

ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD start
