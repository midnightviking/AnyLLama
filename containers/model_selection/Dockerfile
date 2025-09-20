FROM python:3.13-slim-bookworm

# RUN apt-get update && apt-get install -y curl gpg python3-pip
#jump to dir, set in compose though
WORKDIR /app

#copy files
COPY . .

#install requirements
RUN pip install -r requirements.txt 
RUN pip install 'flask[async]'


#admin expose
EXPOSE 5100
ENTRYPOINT [ "/bin/bash", "start.sh" ]