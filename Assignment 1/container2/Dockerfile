FROM python:latest
WORKDIR /container2
COPY . .
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 3000
ENTRYPOINT [ "python" ]
CMD [ "app2.py" ]