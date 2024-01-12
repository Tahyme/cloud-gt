# microservice-deploy-H3

Rapport mi-parcours

Le but du projet est de déployer une application de gestion d'inventaire. Par l'utilisation :
- 1 Dockerfile front => Application flask
- 1 Dockerfile back => SQL server
- => docker-compose.yml pour gerer les deux Dockerfile et le déploiement
- Utilisation d'un nginx quand il sera déployé sur azure
- (+) Implémentation de Kubernetes pour orchestrer les containers docker
- (+) Utilisation de graphana pour faire du monitoring
- (+) Mise en place d'un systeme de gestion de files d'attente
- (+) Mise en place de PowerBI pour une prise d'info via des graphiques


# Architecture

![Schema](https://github.com/BlazingBurn/Microservice_implement_stockManagement/assets/49305403/acc1462e-b6ef-46ef-a7fd-25d87e948d78)

# Route
    => Regarder dans le README.md flask_app

# PROBLEME RENCONTRE

Problemes qui ont ralenti => 
- PC perso qui on ralenti le developpement (Bug, freeze)
- Compatibilité dans le dockerfile entre le back et front (1j d'investigation pour résoudre le probleme)
- Azure => compte hitema impossible de ce connecter avec le mercredi aprem et jeudi

# Docker deployé sur azure

commande utilisé :

    docker build -t stockmanagement .
    docker images
    docker tag stockmanagement testdockerhelloworldh3.azurecr.io/stockmanagement:latest
    docker login testdockerhelloworldh3.azurecr.io
    docker push testdockerhelloworldh3.azurecr.io/stockmanagement

![image](https://github.com/BlazingBurn/Microservice_implement_stockManagement/assets/49305403/3e01fec8-97e0-4cc4-82ac-a5c023fecf13)

# A FAIRE (Dans la semaine si le temps le permet)
- Déployé sur azure
- Ajouter kubernetes

# EXPLICATION BUILD/RUN PROJET

Le projet est build sur Azure et donc automatiquement.

Les liens pour acceder à l'application :
** Lien non disponible puisque l'application n'est plus accesible **
- Ajouter kubernetes
- PowerBI

# SCREEN APP
## / <=> /Overview
![image](https://github.com/BlazingBurn/Microservice_implement_stockManagement/assets/49305403/78514a6e-3deb-4689-a652-9854fc4d8a0c)

## /Product
![image](https://github.com/BlazingBurn/Microservice_implement_stockManagement/assets/49305403/b08d813f-9639-4d10-8aeb-83797dbb26e7)

## /Location
![image](https://github.com/BlazingBurn/Microservice_implement_stockManagement/assets/49305403/7a9f8c8d-f356-419b-b49e-000d1bbae757)

## /Transfers
![image](https://github.com/BlazingBurn/Microservice_implement_stockManagement/assets/49305403/caf3d7f0-1b1c-4e7a-84d6-558df9c6b51b)
