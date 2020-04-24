# Étapes de la mise en ligne

## Configuration de l'espace serveur

![serveur](https://github.com/helenecourau/pur_beurre/blob/master/doc/img/serveur2.png)

Création d'un droplet :
* Image Ubuntu
* Datacenter à Francfort
* Authentification par clé SSH
* Firewall : accès en SSH et par http/https uniquement

Création d'un nouvel utilisateur helene: 

    adduser helene


Utilisateur ajouté dans le groupe des super utilisateurs:

    gpasswd -a helene sudo

Ajout de la clé ssh pour le user helene:

    su – helene
    mkdir .ssh
    chmod 700 .ssh
    nano .ssh/authorized_keys
    chmod 600 .ssh/authorized_keys
    exit

Désactivation de la connexion ssh au root:

    nano /etc/ssh/sshd_config

Dans le fichier on passe la variable PermitRootLogin à no.

On relance:

    service ssh reload


![serveur](https://github.com/helenecourau/pur_beurre/blob/master/doc/img/serveur.png)

## Téléchargement de l'application sur le serveur

Mise à jour et installation des librairies de base:

    sudo apt-get update
    sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib

Récupérer l'application depuis Github: 

    git clone https://github.com/helenecourau/pur_beurre.git

Création de l'environnement virtuel et installation des dépendances: 

    sudo apt install virtualenv
    virtualenv env -p python3
    source env/bin/activate
    pip install -r pur_beurre/requirements.txt

Création de la base de donnée avec un utilisateur:

    sudo -u postgres psql 
    CREATE DATABASE pur_beurre ;
    CREATE USER helene WITH PASSWORD 'un_certain_mdp_mais_je_dirai_pas_quoi';
    ALTER ROLE helene SET client_encoding TO 'utf8';
    ALTER ROLE helene SET default_transaction_isolation TO 'read committed';
    ALTER ROLE helene SET timezone TO 'Europe/Paris';
    GRANT ALL PRIVILEGES ON DATABASE pur_beurre TO helene;

Mise à jour du fichier settings.py avec les informations de connexion à la base de données :

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'pur_beurre',
            'USER': 'helene',
            'PASSWORD': 'un_certain_mdp_mais_je_dirai_pas_quoi',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

Génération des fichiers statiques:
    
    export ENV=PRODUCTION
    python3 manage.py collectstatic

Migration des données:

    python3 manage.py migrate
    python3 manage.py loaddata website/dumps/pur_beurre.json
    python3 manage.py createsuperuser

## Installation et configuration de Nginx

Mise en place du serveur web Nginx pour rediriger les requêtes effectuées sur l'IP publique à l'IP privée. 

Installer Nginx :

    sudo apt-get install nginx

Création d'un fichier de configuration Nginx :

    cd /etc/nginx/
    sudo touch sites-available/pur_beurre

Ajout du lien symbolique pour la prise en compte du fichier de configuration:

    sudo ln -s /etc/nginx/sites-available/pur_beurre /etc/nginx/sites-enabled

Edition du fichier de configuration :

    sudo nano sites-available/pur_beurre

Contenu du fichier de configuration :

    server {

        listen 80; server_name 142.93.109.41;
        root /home/helene/pur_beurre/;

        location /static {
            alias /home/helene/pur_beurre/staticfiles/;
        }

        location / {
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_redirect off;
            if (!-f $request_filename) {
                proxy_pass http://127.0.0.1:8000;
                break;
            }
        }
    }

Modification du fichier settings.py : 

    ALLOWED_HOSTS = ['142.93.109.41']

Relance de Nginx :

    sudo service nginx reload

## Gunicorn

Gunicorn est un serveur http Python pour Unix qui nous permet d'interpréter Django et qui gère le lancement du serveur.

Lancer le processus de serveur de Gunicorn:

    gunicorn pur_beurre.wsgi:application

## Supervisor 

Supervisor permet de lancer ou relancer des services.

Création un fichier de configuration supervisor
    
    sudo apt-get install supervisor
    sudo nano /etc/supervisor/conf.d/pur_beurre-gunicorn.conf

La commande à exécuter pour démarrer Gunicorn :

    command=/home/helene/env/bin/gunicorn pur_beurre.wsgi:application

Fichier de configuration :

    [program:pur_beurre-gunicorn]
    command=/home/helene/env/bin/gunicorn pur_beurre.wsgi:application
    user = helene
    directory = /home/helene/pur_beurre
    autostart = true
    autorestart = true
    environment = ENV="PRODUCTION",SECRET_KEY='secret_key'

Relancer le processus supervisor :

    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl status

## Séparation des environnements

Création de deux fichiers :
* local_settings.py : pour la configuration générale et locale.
* production.py : avec les spécificités de la configuration de production.

Détail du fichier:

    from .local_settings import *
    
    DEBUG = False
    ALLOWED_HOSTS = ['142.93.109.41']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'pur_beurre',
            'USER': 'helene',
            'PASSWORD': 'mdp',
            'HOST': '',
            'PORT': '5432',
        }
    }

Suppression de settings.py

Relancer le processus supervisor :

    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl status
    
    
## Monitoring

![serveur](https://github.com/helenecourau/pur_beurre/blob/master/doc/img/sentry.png)

New Relic et Digital Ocean pour monitorer le serveur et Sentry pour monitorer Django

### DigitalOcean:

J'ai activé des alertes pour surveiller le CPU, l'utilisation de la mémoire vive et de l'espace disque.

    sudo apt-get purge do-agent
    curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash
    /opt/digitalocean/bin/do-agent –version

### NewRelic

![serveur](https://github.com/helenecourau/pur_beurre/blob/master/doc/img/newrelic.png)

    pip install newrelic
    newrelic-admin generate-config <your-key-goes-here> newrelic.ini

Dans le fichier wsgi.py :

    import newrelic.agent
    newrelic.agent.initialize('/home/helene/newrelic.ini')

### Sentry:

    pip install --upgrade 'sentry-sdk==0.14.3'
    import sentry_sdk
    
    
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn="https://12214d63d60c4345922cdb50d617fe69@o359574.ingest.sentry.io/5203503",
        integrations=[DjangoIntegration()],
    )

Tester en faisant une erreur dans le code.

Relancer Gunicorn:

    sudo supervisorctl restart pur_beurre-gunicorn
    
    
## Travis

Travis permet de lancer les tests automatiquement lorsqu'on push le code sur Github.

Fichier de configuration .travis.yml

    language: python
    python:
      - "3.7"
    install:
      - pip install -r requirements.txt
    branches:
      only:
        - master
    env:
      - DJANGO_VERSION=2.0
    services:
      - postgresql
    script:
      - python -m pytest
      - python manage.py test


## Tâche cron

![serveur](https://github.com/helenecourau/pur_beurre/blob/master/doc/img/cron.png)

La tâche cron lance le fichier main.py qui va récupérer les aliments d'OpenFoodFact grâce au fichier resquest_class puis les insérer ou les mettre à jour avec insert_class.

    crontab -e
    00 23 * * 6 /home/helene/env/bin/python /home/helene/pur_beurre/main.py > /home/helene/log.txt 2>&1

