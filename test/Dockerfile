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

# Installe les dépendances Python à partir du fichier requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "python3", "-u", "test.py" ]