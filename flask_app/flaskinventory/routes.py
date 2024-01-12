from flask import  render_template,url_for,redirect,flash,request,jsonify
from flaskinventory import app, es
from flaskinventory.forms import addproduct,addlocation,moveproduct,editproduct,editlocation
from flaskinventory.models import Location,Product,Movement,Balance
from datetime import datetime
import logging

# Configurer les logs
logging.basicConfig(level=logging.DEBUG)

@app.route("/Overview")
@app.route("/")
def overview():
    response = es.search(index='balances', body={'query': {'match_all': {}}})
    balance = response['hits']['hits']
    exists = bool(balance)
    
    if not exists:
        flash(f'Add products, locations, and make transfers to view', 'info')
        
    return render_template('overview.html', balance=balance)

# Route de produit ajout, supression et get
@app.route("/Product", methods = ['GET','POST'])
def product():
    form = addproduct()
    eform = editproduct()
    
    # Utiliser Elasticsearch pour obtenir les détails des produits
    response = es.search(index='products', body={'query': {'match_all': {}}})
    details = response['hits']['hits']

    exists = bool(details)

    if exists == False and request.method == 'GET':
        flash(f'Add products to view', 'info')
        
    
    elif eform.validate_on_submit() and request.method == 'POST':
        p_id = request.form.get("productid", "")
        pname = request.form.get("productname", "")
        details = es.get(index='products', doc_type='_doc', id=p_id)['_source']
        
        # Mettez à jour les détails dans Elasticsearch
        es.update(index='products', doc_type='_doc', id=p_id, body={'doc': {'prod_name': eform.editname.data, 'prod_qty': eform.editqty.data}})
        es.indices.refresh(index='products')  # Rafraîchir l'index

        flash(f'Your product  has been updated!', 'success')
        return redirect('/Product')

    elif form.validate_on_submit():
        product = Product(prod_name=form.prodname.data, prod_qty=form.prodqty.data)
        # Sauvegarder le nouveau produit dans Elasticsearch
        product.save_to_es()
        logging.debug(f"Product added: {product}")

        flash(f'Your product {form.prodname.data} has been added!', 'success')
        es.indices.refresh(index='products') # Rafraîchir l'index
        return redirect('/Product')
        
    return render_template('product.html',title = 'Products', eform=eform, form=form, details=details)

@app.route("/Location", methods = ['GET', 'POST'])
def loc():
    form = addlocation()
    lform = editlocation()
    
    # Utiliser Elasticsearch pour obtenir les détails des emplacements
    response = es.search(index='locations', body={'query': {'match_all': {}}})
    details = response['hits']['hits']
    
    exists = bool(details)
    if exists == False and request.method == 'GET':
        flash(f'Add locations to view', 'info')
            
    
    if lform.validate_on_submit() and request.method == 'POST':
        p_id = request.form.get("locid", "")
        locname = request.form.get("locname", "")
        loc = es.get(index='locations', doc_type='_doc', id=p_id)['_source']

        # Mettez à jour les détails dans Elasticsearch
        es.update(index='locations', doc_type='_doc', id=p_id, body={'doc': {'loc_name': lform.editlocname.data}})
        es.indices.refresh(index='locations')  # Rafraîchissez l'index

        flash(f'Your location has been updated!', 'success')
        return redirect('/Location')

    elif form.validate_on_submit():
        loc = Location(loc_name=form.locname.data)
        # Sauvegarder le nouvel emplacement dans Elasticsearch
        loc.save_to_es()
        es.indices.refresh(index='locations')  # Rafraîchissez l'index

        flash(f'Your location {form.locname.data} has been added!', 'success')
        return redirect('/Location')
    
    return render_template('loc.html', title = 'Locations', lform=lform, form = form, details=details)


@app.route("/Transfers", methods = ['GET', 'POST'])
def move():
    form = moveproduct()

    # Utiliser Elasticsearch pour obtenir les détails des mouvements
    response = es.search(index='movements', body={'query': {'match_all': {}}})
    details = response['hits']['hits']
    
    pdetails = es.search(index='products', body={'query': {'match_all': {}}})['hits']['hits']

    exists = bool(details)
    if exists == False and request.method == 'GET':
        flash(f'Transfer products to view', 'info')
        
    #----------------------------------------------------------
    # Récupérer les choix de produits et d'emplacements depuis Elasticsearch
    prod_choices = [(product['_source']['prod_name'], product['_source']['prod_name']) for product in pdetails]
    loc_choices = [(location['_source']['loc_name'], location['_source']['loc_name']) for location in es.search(index='locations', body={'query': {'match_all': {}}})['hits']['hits']]

    src_list_names, dest_list_names = [('Warehouse', 'Warehouse')], [('Warehouse', 'Warehouse')]
    src_list_names += loc_choices
    dest_list_names += loc_choices
    
    # Passer les listes de noms au formulaire pour les champs de sélection
    form.mprodname.choices = prod_choices
    form.src.choices = src_list_names
    form.destination.choices = dest_list_names
    #--------------------------------------------------------------
    
    # Envoyer à Elasticsearch
    if form.validate_on_submit() and request.method == 'POST':
        timestamp = datetime.now()
        logging.debug(f"Product data : {form.mprodname.data}")
        boolbeans = check(form.src.data, form.destination.data, form.mprodname.data, form.mprodqty.data)

        if boolbeans == False:
            flash(f'Retry with lower quantity than source location', 'danger')
        elif boolbeans == 'same':
            flash(f'Source and destination cannot be the same.', 'danger')
        elif boolbeans == 'no prod':
            flash(f'Not enough products in this location. Please add products', 'danger')
        else:
            # Ajouter le mouvement à Elasticsearch
            es.index(index='movements', doc_type='_doc', body={
                'ts': timestamp,
                'frm': form.src.data,
                'to': form.destination.data,
                'pname': form.mprodname.data,
                'pqty': form.mprodqty.data
            })

            es.indices.refresh(index='movements')  # Rafraîchissez l'index
            flash(f'Your activity has been added!', 'success')

        return redirect(url_for('move'))

    return render_template('move.html', title='Transfers', form = form, details= details)

def check(frm,to,name,qty):
    if frm == to :
        a = 'same'
        return a
    elif frm =='Warehouse' and to != 'Warehouse':
        logging.debug(f"Product name to transfer: {name}")
        prodq = es.search(index='products', body={'query': {'match': {'prod_name': name}}})
        prod_qty = prodq['hits']['hits'][0]['_source']['prod_qty']
        
        logging.debug(f"Product info transf : {prod_qty}")
        
        if prod_qty >= qty:
            # Déduire la quantité du produit de l'entrepôt
            es.update(index='products', id=prodq['hits']['hits'][0]['_id'],
                      body={'doc': {'prod_qty': prod_qty - qty}})

            # Mettre à jour la balance ou ajouter une nouvelle entrée si nécessaire
            bal = es.search(index='balances', body={'query': {'bool': {'must': [
                {'match': {'location': to}},
                {'match': {'product': name}}
            ]}}})

            if not bal['hits']['hits']:
                new = {'product': name, 'location': to, 'quantity': qty}
                es.index(index='balances', doc_type='_doc', body=new)
            else:
                bal_id = bal['hits']['hits'][0]['_id']
                es.update(index='balances', id=bal_id, body={'doc': {'quantity': bal['hits']['hits'][0]['_source']['quantity'] + qty}})

        else:
            return False
        
    elif to == 'Warehouse' and frm != 'Warehouse':
        bal = es.search(index='balances', body={'query': {'bool': {'must': [
            {'match': {'location': frm}},
            {'match': {'product': name}}
        ]}}})

        if not bal['hits']['hits']:
            return 'no prod'
        else:
            # Ajouter la quantité du produit à l'entrepôt
            es.update(index='products', id=bal['hits']['hits'][0]['_id'],
                      body={'doc': {'prod_qty': es.get(index='products', id=bal['hits']['hits'][0]['_source']['product'])['_source']['prod_qty'] + qty}})

            # Déduire la quantité de la balance
            es.update(index='balances', id=bal['hits']['hits'][0]['_id'],
                      body={'doc': {'quantity': bal['hits']['hits'][0]['_source']['quantity'] - qty}})

    else:  # from='?' and to='?'
        bl = es.search(index='balances', body={'query': {'bool': {'must': [
            {'match': {'location': frm}},
            {'match': {'product': name}}
        ]}}})

        if not bl['hits']['hits']:
            return 'no prod'

        elif (bl['hits']['hits'][0]['_source']['quantity'] - 100) > qty:
            # Si la quantité de l'emplacement source est suffisamment grande, vérifier la balance de l'emplacement de destination
            bal = es.search(index='balances', body={'query': {'bool': {'must': [
                {'match': {'location': to}},
                {'match': {'product': name}}
            ]}}})

            if not bal['hits']['hits']:
                # Ajouter une nouvelle entrée pour l'emplacement de destination
                new = {'product': name, 'location': to, 'quantity': qty}
                es.index(index='balances', doc_type='_doc', body=new)

                # Déduire la quantité de l'emplacement source
                es.update(index='balances', id=bl['hits']['hits'][0]['_id'],
                          body={'doc': {'quantity': bl['hits']['hits'][0]['_source']['quantity'] - qty}})
            else:
                # Ajouter à la quantité de l'emplacement de destination et déduire de l'emplacement source
                es.update(index='balances', id=bal['hits']['hits'][0]['_id'],
                          body={'doc': {'quantity': bal['hits']['hits'][0]['_source']['quantity'] + qty}})

                es.update(index='balances', id=bl['hits']['hits'][0]['_id'],
                          body={'doc': {'quantity': bl['hits']['hits'][0]['_source']['quantity'] - qty}})
        else:
            return False

@app.route("/delete")
def delete():
    type = request.args.get('type')
    if type == 'product':
        pid = request.args.get('p_id')
        
        # Supprimer le produit de la base de données Elasticsearch
        es.delete(index='products', id=pid)
        
        flash(f'Your product has been deleted!', 'success')
        return redirect(url_for('product'))
    else:
        pid = request.args.get('p_id')
        
        # Supprimer l'emplacement de la base de données Elasticsearch
        es.delete(index='locations', id=pid)
        
        flash(f'Your location has been deleted!', 'success')
        return redirect(url_for('loc'))