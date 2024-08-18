FROM python:3-alpine
WORKDIR /usr/ping-pong
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 3001
RUN pip3 install -r requirements.txt #&& adduser -D johndoe && chown -R johndoe /usr /usr/persist/output
#USER johndoe
CMD ["python3", "server.py"]