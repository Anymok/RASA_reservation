# Utilisation d'une image de base avec Python
FROM python:3.10-slim

# Spécifier le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . .

# Installation des dépendances du projet
RUN pip install rasa

# Exposer le port utilisé par Rasa (5005 par défaut)
EXPOSE 5005

# Commande par défaut à exécuter lorsque le conteneur est démarré
CMD ["rasa", "run", "-m", "models --enable-api --cors '*' --debug"]
