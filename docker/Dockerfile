from python:alpine

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone https://github.com/danhidsan/decide-ganimedes-almacenamiento .
RUN pip install -r requirements.txt

# change work directory
WORKDIR /app/decide

# adding local settings
ADD docker-settings.py /app/decide/local_settings.py
RUN ./manage.py collectstatic
