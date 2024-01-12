# Inventory-Manager
An inventory management system using Flask

### Prerequisites

To run this system you will need :

- Python 3
- Flask
- SQLALCHEMY
- WTForms

Assuming you have Python, proceed to install the rest using the command below:

```
pip3 install -r requirements.txt
```

# Built using
- Flask
- SQLAlchemy

# License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

# Endpoint

- /Overview <=> /
- /Product
- /Location
- /Transferts
- /delete

## GET

    - /Overview => Affiche un produit, la quantité ainsi que la localisation
    - /Product => Affiche tout les produits renseignés
    - /Location => Affiche toutes les locations renseignés

## POST

    - /Product => Bouton "post" qui va ajouter un produit
    - /Location => Bouton "post" qui va ajouter une location
    - /Transfers => Bouton "move product" qui va ajouter un transfert

## UPDATE

    - /Product => Bouton "edit" qui udpate un produit
    - /Location => Bouton "edit" qui udpate une location

## DELETE

    - /Product => bouton "delete" qui sup un produit
    - /Location => bouton "delete" qui sup une location