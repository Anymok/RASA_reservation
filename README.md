# Requirements
 - Visual Studio Code or an IDE
 - Python 3.10



# Setup
 - Open project with your IDE
 - Open terminal and execute :
    - py -3.10 -m venv .env
    - .\.env\Scripts\activate
    - pip3 install -r .\requirements.txt
    - py -m rasa train



# Start tchating with bot
 - Open project with your IDE
 - Open terminal and execute :
    - .\.env\Scripts\activate
    - py -m rasa shell
 - Open second terminal and execute :
   - .\.env\Scripts\activate
   - py -m rasa run actions



# FONCTIONNALITE

OK :

    - Réserver une table
    - Annuler une réservation
    - Afficher information réservation et modifier commentaire
    - Obtenir la liste des allergènes
    - Obtenir le menu du jour
    - Obtenir le liens vers le menu complet
    - Date de réservation, Nombre de personnes, Nom de réservation, Numéro de téléphone
    - Ajouter un commentaire à la réservation
    - Vérifier si disponible
    - Obtenir un numéro de réservation
    - Fournir l’ensemble des fichiers sur un git(hub/lab/autre), bonus si usage d’image docker ! 

  
NON VALIDE :

    - Intégrer le bot sur une plateforme

# BUG

    - Commentaire : Il faut mettre un message comme dans les intents sinon il est pas reconnu
    - Base de données : Certain wifi bug l'accès à la BDD (comme l'EPSI :) )
    - Mélange avec les numéros : parfois le bot se mélange lorsque l'on saisit un numéro et perd la story. La solution est de regarder les intents et essayer de rajouter des mots pour être plus précis.
    


