# Documents et notebooks

Ce dossier reprend le contenu de `spark/notebooks` du dépôt FormationBigDataBI. Les notebooks, scripts, cartes et documents sont gardés dans leur arborescence d’origine. Le guide source est conservé dans [README-source.md](README-source.md).

JupyterLab rend ce dossier disponible sous `/workspace/notebooks`. Spark tourne en mode local dans le conteneur `spark-lab`. Pour lancer les services, consultez le [guide général](../README.md).

RustFS est également démarré pour les exercices S3. Il est accessible depuis les conteneurs avec l’URL `http://rustfs:9000` et depuis l’hôte avec `http://localhost:9000`. Les buckets ne sont pas créés et aucun fichier n’est chargé automatiquement.

Certains supports d’origine peuvent supposer des fichiers ou des services absents de cette version simplifiée. Les exercices concernés devront être adaptés à votre environnement avant leur exécution.
