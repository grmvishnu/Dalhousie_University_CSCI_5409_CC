FROM python:latest
WORKDIR /container1
COPY . .
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app1.py" ]