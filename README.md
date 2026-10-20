# SimpleBigDataBI

Environnement pédagogique Big Data et BI réduit, lancé avec Docker Compose.

## Contenu

- **PostgreSQL** pour les exercices SQL et la préparation de tables analytiques.
- **Kafka** en mode KRaft pour découvrir les flux d’événements.
- **Spark et JupyterLab** pour les traitements batch et l’exploration avec PySpark.
- **RustFS** pour les exercices de stockage objet compatibles S3.
- **Portail local** pour retrouver les adresses de connexion, comptes et tokens actifs.
- **Power BI** peut se connecter à PostgreSQL depuis la machine hôte.

Les documents Spark du dépôt source sont repris dans `notebooks/`. Le projet ne requiert pas de répertoire local de jeux de données et ne copie ni ne charge automatiquement de fichiers vers RustFS. Les exemples peuvent s’appuyer sur des données créées dans PostgreSQL ou sur des fichiers que vous ajoutez vous-même.

## Prérequis

Docker Desktop avec Docker Compose v2, ou Docker Engine avec le plugin Compose.

## Démarrer

À la racine du dépôt :

```bash
docker compose --env-file .env.example --env-file ports.env up -d --build
docker compose --env-file .env.example --env-file ports.env ps
```

Ouvrir le portail sur [http://localhost:25021](http://localhost:25021). Il affiche dans des cartes les comptes et tokens transmis aux services par `.env.example`, avec des liens vers JupyterLab et RustFS. Les secrets sont affichés en clair dans ce portail ; il est destiné à un usage local.

Pour personnaliser les comptes et tokens, copiez `.env.example` vers `.env`, modifiez les valeurs, puis remplacez `--env-file .env.example` par `--env-file .env` dans les commandes ci-dessus. Pour adapter les ports publiés sur la machine, modifiez `ports.env`.

Tous les ports publiés par Compose sont liés à `127.0.0.1` : le portail et les services sont accessibles depuis la machine locale uniquement.

## Connexions

| Outil | Adresse |
|---|---|
| Portail et identifiants | http://localhost:25021 |
| JupyterLab | http://localhost:8888 |
| PostgreSQL depuis l’hôte | localhost:5432 |
| Kafka depuis l’hôte | localhost:9092 |
| Kafka depuis les conteneurs | kafka:19092 |
| API S3 RustFS | http://localhost:9000 |
| Console RustFS | http://localhost:9001 |

Accès RustFS par défaut : clé `labadmin`, secret `TRAINING_ONLY_S3_PASSWORD`. Ces identifiants sont prévus pour un usage local de formation. Aucun bucket ni chargement de fichiers n’est configuré automatiquement.

Paramètres PostgreSQL par défaut : base `formation`, utilisateur `formation`, mot de passe `formation`. Pour Power BI Desktop, choisir le connecteur PostgreSQL et utiliser `localhost:5432`.

## Exemple Spark

Le script crée un petit jeu de données en mémoire et affiche une agrégation :

```bash
docker compose --env-file .env.example --env-file ports.env exec spark-lab python /workspace/jobs/hello_spark.py
```

Les notebooks locaux sont montés dans `notebooks/`. Pour arrêter les services :

```bash
docker compose --env-file .env.example --env-file ports.env down
```

Pour supprimer aussi les volumes PostgreSQL, Kafka et RustFS :

```bash
docker compose --env-file .env.example --env-file ports.env down -v
```
