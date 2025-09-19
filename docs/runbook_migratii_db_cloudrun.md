## Runbook: Migrații DB pentru Cloud SQL (Cloud Run Job + alternativ local)

Scop: aplici migrațiile Alembic pe instanța Cloud SQL, fără să-ți bați capul cu conexiunea locală. Varianta recomandată: Job pe Cloud Run (folosește Cloud SQL Connector). Alternativ: local cu Cloud SQL Proxy.

### Varianta recomandată: Job pe Cloud Run

1) Setează variabilele (PowerShell)
```powershell
$PROJECT = "trading-472212"
$REGION = "us-central1"
$INSTANCE = "${PROJECT}:${REGION}:trading-postgres"
$IMAGE = "gcr.io/$PROJECT/trading-api:v19"   # imaginea curentă a serviciului
$SA = "svc-cloudrun@$PROJECT.iam.gserviceaccount.com"
# DSN cu driver psycopg v3 (atenție: NU folosi postgresql:// implicit)
$DBURL = "postgresql+psycopg://postgres:POSTGRES_PASSWORD@/trading?host=/cloudsql/$INSTANCE"
```

2) Creează jobul (o singură dată)
```powershell
gcloud run jobs create migrate-db `
  --image $IMAGE `
  --region $REGION `
  --service-account $SA `
  --set-cloudsql-instances $INSTANCE `
  --set-env-vars "DATABASE_URL=$DBURL" `
  --command alembic `
  --args upgrade,head
```

Dacă jobul există deja, folosește update:
```powershell
gcloud run jobs update migrate-db `
  --image $IMAGE `
  --region $REGION `
  --service-account $SA `
  --set-cloudsql-instances $INSTANCE `
  --set-env-vars "DATABASE_URL=$DBURL" `
  --command alembic `
  --args upgrade,head
```

3) Rulează migrarea
```powershell
gcloud run jobs execute migrate-db --region $REGION
```

4) Verifică execuția și logurile
```powershell
$EXEC = gcloud run jobs executions list --job migrate-db --region $REGION --format="value(name)" | Select-Object -First 1
gcloud run jobs executions describe $EXEC --region $REGION --format="value(status.conditions[-1].message)"

gcloud logging read `
  "resource.type=cloud_run_job AND resource.labels.job_name=migrate-db AND resource.labels.region=$REGION" `
  --limit=200 --format="value(textPayload)"
```

Semn de reușită: condiția finală „Completed” și în loguri se vede Alembic rulând „upgrade head” fără erori.

Notă:
- Jobul folosește Cloud SQL Connector din Cloud Run. Nu e nevoie de IP public și nici de autorizații de rețea deschise.
- DSN-ul trebuie să fie `postgresql+psycopg://...` (psycopg v3). Evită `postgresql://...` (psycopg2) ca să nu primești `ModuleNotFoundError: psycopg2`.

Opțional: Ștergere job
```powershell
gcloud run jobs delete migrate-db --region $REGION
```

### Alternativ (doar dacă ai nevoie local): Cloud SQL Proxy + Alembic

1) Descarcă proxy-ul (Windows)
```powershell
cd D:\CODEX\Trading
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
curl.exe -L -o cloud-sql-proxy.exe https://github.com/GoogleCloudPlatform/cloud-sql-proxy/releases/download/v2.12.0/cloud-sql-proxy-x64.exe
```
În caz de probleme cu GitHub, fallback:
```powershell
curl.exe -L -o cloud-sql-proxy.exe https://dl.google.com/cloudsql/cloud_sql_proxy_x64.exe
```

2) Pornește proxy-ul (ține fereastra deschisă)
```powershell
./cloud-sql-proxy.exe --gcloud-auth --port 5432 ${PROJECT}:${REGION}:trading-postgres
```

3) Rulează Alembic într-o fereastră nouă
```powershell
cd D:\CODEX\Trading\server
$env:DATABASE_URL = "postgresql+psycopg://postgres:POSTGRES_PASSWORD@127.0.0.1:5432/trading"
alembic upgrade head
```

### Troubleshooting rapid
- `ModuleNotFoundError: psycopg2` → DSN greșit. Folosește `postgresql+psycopg://...` (psycopg v3).
- Job „NOT_FOUND” la execute → nu a fost creat sau regiunea greșită. Creează jobul și verifică `$REGION`.
- Download proxy eșuat → folosește fallback-ul `dl.google.com` sau descarcă manual în folder și rulează.

### Observații de securitate
- Nu comite parole reale în repo. Înlocuiește `POSTGRES_PASSWORD` cu secret manager / variabile de mediu la runtime.
- Pe instanța Cloud SQL, ține lista de rețele autorizate goală; rely doar pe Cloud SQL Connector.


