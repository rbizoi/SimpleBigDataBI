# SimpleBigDataBI

Environnement pédagogique Big Data et BI réduit, lancé avec Docker Compose.

## Contenu

- **PostgreSQL** pour les exercices SQL et la préparation de tables analytiques.
- **Kafka et Kafka UI** pour les flux d’événements et leur supervision.
- **Cluster Spark 4.0.4** avec un maître, deux ouvriers, Spark History Server et JupyterLab.
- **RustFS** pour les exercices de stockage objet compatibles S3.
- **Portail local** pour retrouver les adresses de connexion, comptes et tokens.
- **Power BI** peut se connecter à PostgreSQL depuis la machine hôte.

Les documents Spark du dépôt source sont repris dans `notebooks/`. Les notebooks Jupyter sont connectés au cluster Spark. Spark est configuré pour joindre Kafka et RustFS depuis le réseau Compose, avec S3A. Aucun bucket ni fichier n’est créé ou chargé automatiquement dans RustFS ; créez vous-même un bucket depuis sa console pour les exercices S3.

Le projet n’utilise pas de répertoire local de jeux de données. Les données d’exemple peuvent être créées dans PostgreSQL ou ajoutées manuellement dans les notebooks.

## Prérequis

Docker Desktop avec Docker Compose v2, ou Docker Engine avec le plugin Compose. Prévoir au moins 12 Go de mémoire disponibles pour Docker pour l’ensemble du cluster et des services associés.

## Démarrer

À la racine du dépôt :

```bash
docker compose --env-file .env.example --env-file ports.env up -d --build
docker compose --env-file .env.example --env-file ports.env ps
```

Ouvrir le portail sur [http://localhost:25021](http://localhost:25021). Il affiche les comptes et tokens chargés depuis `.env.example`, ainsi que les liens vers les interfaces Spark, Kafka UI, JupyterLab et RustFS. Les secrets sont affichés en clair ; le portail est destiné à un usage local.

Pour personnaliser les comptes et tokens, copiez `.env.example` vers `.env`, modifiez les valeurs, puis remplacez `--env-file .env.example` par `--env-file .env` dans les commandes. Pour adapter les ports hôte, modifiez `ports.env`.

Tous les ports publiés par Compose sont liés à `127.0.0.1` et accessibles depuis la machine locale uniquement.

## Interfaces et connexions

| Service | Adresse hôte |
|---|---|
| Portail | http://localhost:25021 |
| PostgreSQL | localhost:25001 |
| Kafka | localhost:25002 |
| API S3 RustFS | http://localhost:25003 |
| Console RustFS | http://localhost:25004 |
| Spark Master UI | http://localhost:25006 |
| Spark Worker 1 UI | http://localhost:25007 |
| Spark Worker 2 UI | http://localhost:25008 |
| Spark History Server | http://localhost:25009 |
| JupyterLab | http://localhost:25010 |
| Spark Jobs UI (Jupyter) | http://localhost:25011 |
| Kafka UI | http://localhost:25018 |

Depuis les conteneurs, Kafka est accessible à `kafka:19092` et RustFS à `http://rustfs:9000`. La console RustFS utilise la clé `labadmin` et le secret `TRAINING_ONLY_S3_PASSWORD` par défaut. Le token Jupyter par défaut est `formation`. Ces valeurs sont destinées à un environnement local de formation.

Les notebooks sont montés dans JupyterLab depuis `notebooks/`. Pour arrêter les services :

```bash
docker compose --env-file .env.example --env-file ports.env down
```

Pour supprimer aussi les volumes persistants :

```bash
docker compose --env-file .env.example --env-file ports.env down -v
```
