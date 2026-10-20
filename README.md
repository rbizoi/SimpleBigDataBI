# SimpleBigDataBI

Environnement pédagogique Big Data et BI réduit, lancé avec Docker Compose.

## Contenu

- **PostgreSQL** pour les exercices SQL et la préparation de tables analytiques.
- **Kafka** en mode KRaft pour découvrir les flux d’événements.
- **Spark et JupyterLab** pour les traitements batch et l’exploration avec PySpark.
- **Power BI** peut se connecter à PostgreSQL depuis la machine hôte.

Le projet ne requiert aucun dossier local de jeux de données. Les exercices peuvent partir de données créées dans PostgreSQL ou de fichiers que vous placez vous-même dans `notebooks/`. Aucun chargement automatique vers un stockage objet n’est configuré.

## Prérequis

Docker Desktop avec Docker Compose v2, ou Docker Engine avec le plugin Compose.

## Démarrer

À la racine du dépôt :

```bash
docker compose up -d
docker compose ps
```

Ouvrir JupyterLab sur [http://localhost:8888](http://localhost:8888). Le jeton par défaut est `formation`.

Pour personnaliser les identifiants ou les ports, copier `.env.example` vers `.env`, puis modifier les valeurs avant le démarrage.

## Connexions

| Outil | Adresse |
|---|---|
| JupyterLab | http://localhost:8888 |
| PostgreSQL depuis l’hôte | localhost:5432 |
| Kafka depuis l’hôte | localhost:9092 |
| Kafka depuis les conteneurs | kafka:19092 |

Paramètres PostgreSQL par défaut : base `formation`, utilisateur `formation`, mot de passe `formation`. Ils sont destinés à un usage local de formation.

Pour Power BI Desktop, choisir le connecteur PostgreSQL et utiliser `localhost:5432`.

## Exemple Spark

Le script crée un petit jeu de données en mémoire et affiche une agrégation :

```bash
docker compose exec spark-lab python /workspace/jobs/hello_spark.py
```

Les notebooks locaux sont montés dans `notebooks/`. Pour arrêter les services :

```bash
docker compose down
```

Pour supprimer aussi les tables PostgreSQL enregistrées dans le volume Compose :

```bash
docker compose down -v
```
