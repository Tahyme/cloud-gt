# Utilisation de l'image officielle Elasticsearch
FROM docker.elastic.co/elasticsearch/elasticsearch:7.10.1

# Copier le fichier de configuration personnalisé
COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

# Exposer le port d'Elasticsearch
EXPOSE 9200

# CMD spécifique à Elasticsearch
CMD ["/usr/local/bin/docker-entrypoint.sh"]