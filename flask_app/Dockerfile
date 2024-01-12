# syntax=docker/dockerfile:1

# Utilisation d'une image de base Ubuntu en 20.04
FROM ubuntu:20.04

# Mettre à jour le système et installer Python 3.8
RUN apt-get update && apt-get install -y python3.8 python3-pip

# Créer un lien symbolique pour python3.8 (peut ne pas être nécessaire)
RUN ln -s /usr/bin/python3.8 /usr/bin/python

# Défini la variable d'environnement SHELL
SHELL ["/bin/bash", "-c"]

# Défini le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt requirements.txt

# Installez les bibliothèques ODBC (unixodbc et unixodbc-dev)
# RUN apt-get install -y unixodbc unixodbc-dev

# Installer lsb-release
RUN apt-get update && apt-get install -y lsb-release

# Définir la variable d'environnement TERM
ENV TERM=xterm

# ADD ODBC Driver 18
# RUN apt-get update && apt-get -y install curl
# COPY odbc18install.sh /app/
# RUN chmod +x /app/odbc18install.sh && /app/odbc18install.sh

# Installe les dépendances Python à partir du fichier requirements.txt
RUN pip3 install -r requirements.txt

# Copie le contenu de l'application dans le conteneur
COPY . /app

# Défini la variable d'environnement FLASK_APP
ENV FLASK_APP run.py

# Expose le port 5000 pour Flask
EXPOSE 5000

# Démarre l'application Flask lorsque le conteneur est lancé
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
