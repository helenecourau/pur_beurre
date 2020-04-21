### Étapes de la mise en ligne

## Configuration de l'espace serveur

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
logout

Désactivation de la connexion ssh au root:
nano /etc/ssh/sshd_config
Dans le fichier on passe la variable PermitRootLogin à no
on relance:
service ssh reload

## Téléchargement de l'application sur le serveur

Mise à jour et installation des libraires de base
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
Voir comment on peut récupérer ou envoyer sur git
Récupérer l'application depuis git 
git clone votredepot.git
Création de l'environnement virtuel et installation des dépendances : 
sudo apt install virtualenv
virtualenv env -p python3
source env/bin/activate
pip install -r pur_beurre/requirements.txt
Création de la base de donnée avec un utilisateur
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
Génération des fichiers statiques
export ENV=PRODUCTION
python3 manage.py collectstatic
Migration des données
python3 manage.py migrate
python3 manage.py loaddata website/dumps/pur_beurre.json
python3 manage.py createsuperuser

Nginx
Vous allez configurer un logiciel pour transférer les requêtes effectuées sur l'IP (148.312.124.4) publique à l'IP privée(http://127.0.0.1:8000/). Il s'agit d'un serveur web ou serveur HTTP.
Installer nginx :
sudo apt-get install nginx
création d'un fichier de configuration Nginx
sudo touch sites-available/pur_beurre
Ajout du lien symbolique pour la prise en compte du fichier de configuration
sudo ln -s /etc/nginx/sites-available/pur_beurre /etc/nginx/sites-enabled
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
la directive location prend deux paramètres : l'URI et les directives à appliquer. Ici, j'indique que toute URI commençant par / doit être redirigée vers l'URL http://127.0.0.1:8000. De fait, toutes les URL seront donc traitées par l'application Django.

proxy_set_header réécrit les headers de la requête HTTP. X-Forwarded-For transmet l'adresse IP du client qui a fait la requête originale. Ces lignes sont nécessaires pour que Django ait toutes les informations nécessaires. 
settings.py : ALLOWED_HOSTS = ['142.93.109.41'] 
sudo service nginx reload

Gunicorn
Il s'agit d'un serveur HTTP Python pour Unix qui utilise les spécifications WSGI (Web Server Gateway Interface). 
Gunicorn est un logiciel en ligne de commande qui se démarre directement depuis le terminal. 
gunicorn pur_beurre.wsgi:application

Supervisor 
pour s'assurer que Gunicorn tourne bien et le relancer en cas de problème
créer un fichier de configuration supervisor
sudo nano /etc/supervisor/conf.d/pur_beurre-gunicorn.conf
la commande à exécuter pour démarrer Gunicorn
command=/home/helene/env/bin/gunicorn pur_beurre.wsgi:application
ensemble du fichier de configuration :
[program:pur_beurre-gunicorn]
command=/home/helene/env/bin/gunicorn pur_beurre.wsgi:application
user = helene
directory = /home/helene/pur_beurre
autostart = true
autorestart = true
environment = ENV="PRODUCTION",SECRET_KEY='secret_key'
relancer le processus supervisor :
supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status

Monitoring du serveur

Surveiller la mémoire vide, la bande passante
Commande top pour regarder ça depuis la console
New Relic et Digital Ocean pour monitorer le serveur et Sentry pour monitorer Django
DigitalOcean :
sudo apt-get purge do-agent
curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash
/opt/digitalocean/bin/do-agent –version
Sentry : new project, 
pip install --upgrade 'sentry-sdk==0.14.3'
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://12214d63d60c4345922cdb50d617fe69@o359574.ingest.sentry.io/5203503",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
Faire une erreur
sudo supervisorctl restart pur_beurre-gunicorn

NewRelic
pip install newrelic
newrelic-admin generate-config <your-key-goes-here> newrelic.ini
wsgi.py :
import newrelic.agent
newrelic.agent.initialize('/home/helene/newrelic.ini')
