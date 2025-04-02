FROM harbor.d4science.org/ccp-runtimes/cookie-cutter:1.0.0

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY deploy.sh __main__.py ./
RUN chmod 755 deploy.sh

CMD ["sh", "-c", "./deploy.sh ; python ."]