FROM harbor.d4science.org/ccp-runtimes/cookie-cutter:1.0.0

COPY DejaVuSans.ttf ./

COPY requirements.txt train.py predict.py train.sh predict.sh ./
RUN chmod 755 *.sh
RUN pip install -r requirements.txt