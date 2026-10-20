from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import quote


def value(name: str, default: str) -> str:
    return os.environ.get(name, default)


def e(text: str) -> str:
    return escape(text, quote=True)


def card(title: str, subtitle: str, fields: list[tuple[str, str, str]], links: list[tuple[str, str]]) -> str:
    rows = "".join(
        '<div class="field"><span>' + e(label) + '</span><code>' + e(val) + '</code>'
        + '<button class="copy" type="button" aria-label="Copier ' + e(label) + '" data-copy="' + e(val) + '">Copier</button></div>'
        for label, val, _kind in fields
    )
    anchors = "".join('<a class="service-link" href="' + e(url) + '" target="_blank" rel="noreferrer">' + e(label) + ' ↗</a>' for label, url in links)
    return '<article class="card"><div class="card-head"><div><p class="eyebrow">SERVICE LOCAL</p><h2>' + e(title) + '</h2><p class="subtitle">' + e(subtitle) + '</p></div><span class="badge">Configuré</span></div><div class="fields">' + rows + '</div><div class="links">' + anchors + '</div></article>'


def page() -> bytes:
    pg_port = value("POSTGRES_PORT", "25001")
    kafka_port = value("KAFKA_PORT", "25002")
    jupyter_port = value("JUPYTER_PORT", "25010")
    kafka_ui_port = value("KAFKA_UI_PORT", "25018")
    spark_master_port = value("SPARK_MASTER_UI_PORT", "25006")
    spark_worker1_port = value("SPARK_WORKER1_UI_PORT", "25007")
    spark_worker2_port = value("SPARK_WORKER2_UI_PORT", "25008")
    spark_history_port = value("SPARK_HISTORY_UI_PORT", "25009")
    spark_jobs_port = value("SPARK_JOBS_UI_PORT", "25011")
    jupyter_token = value("JUPYTER_TOKEN", "formation")
    s3_api_port = value("S3_API_PORT", "25003")
    s3_console_port = value("S3_CONSOLE_PORT", "25004")
    s3_key = value("S3_ACCESS_KEY", "labadmin")
    s3_secret = value("S3_SECRET_KEY", "TRAINING_ONLY_S3_PASSWORD")
    db = value("POSTGRES_DB", "formation")
    user = value("POSTGRES_USER", "formation")
    password = value("POSTGRES_PASSWORD", "formation")

    cards = "".join([
        card("PostgreSQL", "Base et compte de connexion", [("Hôte", "localhost:" + pg_port, ""), ("Base", db, ""), ("Utilisateur", user, ""), ("Mot de passe", password, "")], []),
        card("JupyterLab · Spark", "Espace de notebooks", [("Jeton actif", jupyter_token, "")], [("Ouvrir JupyterLab", "http://localhost:" + jupyter_port + "/lab?token=" + quote(jupyter_token, safe=""))]),
        card("RustFS", "Stockage objet compatible S3", [("Clé d’accès", s3_key, ""), ("Secret", s3_secret, ""), ("Région", value("AWS_REGION", "us-east-1"), "")], [("API S3", "http://localhost:" + s3_api_port), ("Console", "http://localhost:" + s3_console_port)]),
        card("Kafka", "Broker de messages · sans authentification", [("Adresse hôte", "localhost:" + kafka_port, ""), ("Adresse conteneur", "kafka:19092", "")], [("Ouvrir Kafka UI", "http://localhost:" + kafka_ui_port)]),
        card("Cluster Spark", "Maître, deux ouvriers et historique des traitements", [], [("Maître", "http://localhost:" + spark_master_port), ("Ouvrier 1", "http://localhost:" + spark_worker1_port), ("Ouvrier 2", "http://localhost:" + spark_worker2_port), ("Historique", "http://localhost:" + spark_history_port), ("Jobs Jupyter", "http://localhost:" + spark_jobs_port)]),
    ])
    html = '''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer"><title>SimpleBigDataBI · Portail local</title>
<style>
:root{color-scheme:light;--ink:#172b4d;--muted:#62718a;--line:#dce4ef;--blue:#235ee7;--bg:#f3f6fb;--green:#19734a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.top{background:#102342;color:white;padding:32px max(24px,calc((100vw - 1120px)/2)) 38px}.topline{display:flex;align-items:center;gap:12px;color:#b6c9e8;font-size:13px;font-weight:650;letter-spacing:.08em;text-transform:uppercase}
.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:10px;background:#2c67e9;color:white;font-weight:800}.top h1{margin:22px 0 6px;font-size:clamp(27px,4vw,38px);letter-spacing:-.035em}.top p{max-width:680px;margin:0;color:#c0cde0}
main{max-width:1120px;margin:28px auto 64px;padding:0 24px}.notice{display:flex;gap:12px;align-items:flex-start;padding:15px 17px;background:#eaf1ff;border:1px solid #d7e4ff;border-radius:12px;color:#294772;margin-bottom:20px}.notice strong{display:block}.notice p{margin:2px 0 0;color:#526887;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.card{background:white;border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:0 4px 16px #172b4d08}.card-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.eyebrow{font-size:10px;letter-spacing:.12em;color:#71829a;font-weight:750;margin:0 0 5px}.card h2{font-size:20px;margin:0;letter-spacing:-.02em}.subtitle{color:var(--muted);font-size:13px;margin:3px 0 0}.badge{white-space:nowrap;color:var(--green);background:#e7f6ee;border-radius:999px;padding:5px 9px;font-size:11px;font-weight:700}
.fields{margin:18px 0 8px}.field{display:grid;grid-template-columns:minmax(90px,1fr) minmax(90px,1.35fr) auto;align-items:center;gap:8px;padding:9px 0;border-top:1px solid #edf1f6}.field span{font-size:12px;color:var(--muted)}.field code{font:12px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;overflow-wrap:anywhere;color:#243955}.copy{border:0;background:transparent;color:var(--blue);font-size:11px;font-weight:700;cursor:pointer;padding:4px}.copy:hover{text-decoration:underline}
.links{display:flex;flex-wrap:wrap;gap:8px;margin-top:15px}.service-link{color:var(--blue);text-decoration:none;font-size:12px;font-weight:700;padding:8px 10px;border:1px solid #dce7ff;border-radius:8px;background:#f7f9ff}.service-link:hover{background:#eaf1ff}.foot{font-size:12px;color:var(--muted);margin-top:20px}
@media(max-width:700px){.grid{grid-template-columns:1fr}.top{padding:25px 22px 30px}main{padding:0 16px;margin-top:18px}.field{grid-template-columns:85px minmax(0,1fr) auto}}
</style></head><body><header class="top"><div class="topline"><span class="mark">SB</span> Formation Big Data &amp; BI</div><h1>Votre environnement local</h1><p>Accès aux services et identifiants configurés pour cette machine. Les valeurs sont celles transmises par la configuration Docker Compose.</p></header>
<main><section class="notice"><span aria-hidden="true">🔒</span><div><strong>Portail accessible uniquement depuis cet ordinateur</strong><p>Les ports des services et du portail sont liés à localhost. Gardez cette page privée : elle affiche les secrets actifs de votre environnement.</p></div></section>
<section class="grid">''' + cards + '''</section><p class="foot">Les identifiants proviennent du fichier d’environnement chargé par Compose (par défaut, .env.example).</p></main>
<script>document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(b.dataset.copy);b.textContent='Copié';setTimeout(()=>b.textContent='Copier',1200)}catch{b.textContent='Copie indisponible';setTimeout(()=>b.textContent='Copier',1600)}}));</script>
</body></html>'''
    return html.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        body = page()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Do not log request details alongside a page that displays credentials.
        return


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8090), Handler).serve_forever()