# Custom Shields.io Creator

Minimal Flask app for generating Shields.io badge URLs with a web UI and a lightweight REST API.

## Objetivo do projeto

- MVP simples com pretensão de escalar: demonstrar um ciclo de vida end-to-end (desenvolvimento → build → imagem container → deploy) com baixo custo operacional e máxima portabilidade.

## Arquitetura do projeto

- Backend: `Flask` serve o template e endpoints mínimos:
  - `/` UI estática
  - `/api/healthz` health check (GET)
  - `/api/generate` geração programática de URL do badge (POST)
- Frontend: arquivos estáticos em `App/static` com `app.js` (lógica UI) e Tailwind (`input.css` → `output.css`).
- Build & Run: `package.json` contém scripts Tailwind; `Dockerfile` e `compose.yaml` permitem execução reproduzível.

## Decisões técnicas

- Simplicidade primeiro: poucas rotas, lógica estateless e validação mínima. Isso reduz superfície de bugs e facilita escalar horizontalmente.
- Eficiência: assets estáticos servidos diretamente pelo Flask (ou por proxy/CND em produção); CSS gerado em build para evitar processamento runtime.
- Portabilidade: containerização com Docker para garantir que o mesmo artefato rode localmente e em provedores (Cloud Run, Render, Fly, etc.).

## Simplicidade e eficiência — por que funciona

- A aplicação faz pouco: monta uma URL para `img.shields.io` com base em entradas do usuário. Como não armazena estado, é simples replicá-la.
- A separação UI/API permite que consumidores programáticos (scripts, CI/CD, bots) usem a função via HTTP sem depender da interface web.

## Funcionamento (por trás dos panos)

1. O servidor Flask é inicializado por `main.py`; `App/__init__.py` configura a app e importa as rotas (`App/routes.py`).
2. A rota `/` entrega `App/templates/index.html`, que carrega `App/static/app.js` e `output.css`.
3. `app.js` atualiza o preview montando a URL do badge (ex.: `https://img.shields.io/badge/LABEL-MESSAGE-COLOR?...`).
4. `POST /api/generate` recebe JSON, valida `message` (obrigatório), monta a URL usando `urllib.parse` e devolve JSON `{ "url": "..." }`.
5. `GET /api/healthz` retorna `{ "status": "ok" }` usado para health/readiness.

---

## Tutorial de uso

### Pré-requisitos

- Python 3.11+ (ou 3.12)
- Node.js (para Tailwind)
- Docker (opcional, recomendado para testes e deploy)

### Rodando local (venv)

PowerShell:

```powershell
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
npm install
npm run build:css
$env:APP_HOST='127.0.0.1'; $env:APP_PORT='5000'; python main.py
```

Bash/macOS:

```bash
source venv/bin/activate
pip install -r requirements.txt
npm install
npm run build:css
APP_HOST=127.0.0.1 APP_PORT=5000 python main.py
```

Abra no navegador: `http://127.0.0.1:5000`

### Usando Docker (rápido e reproduzível)

Build da imagem:

```bash
docker build -t custom-shields-creator .
```

Rodar container:

```bash
docker run --rm -d -p 5000:5000 --name custom-shields-creator custom-shields-creator
```

Ou com Compose:

```bash
docker compose up --build -d
# parar

docker compose down
```

### Testes / API

Health (GET):

```bash
curl -sS http://127.0.0.1:5000/api/healthz
# => {"status":"ok"}
```

Generate (POST):

```bash
curl -sS -X POST http://127.0.0.1:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"label":"BUILD","message":"PASSING","color":"brightgreen","style":"flat","logo":"github"}'
```

Resposta esperada:

```json
{"url":"https://img.shields.io/badge/BUILD-PASSING-brightgreen?style=flat&logo=github"}
```

PowerShell exemplo:

```powershell
$body = @{ label='BUILD'; message='PASSING'; color='brightgreen' } | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/api/generate" -ContentType "application/json" -Body $body
```

### Teste rápido automatizado

- Há um script `test-local.ps1` que tenta `healthz`, `generate` e, se necessário, inicia o container via Docker.

---

## Observações para evolução/entrevista

- O design é intencionalmente minimal para demonstrar princípios: API bem definida, stateless, container-ready e com testes de smoke.
- Para produção: adicionar proxy reverso (Nginx/Caddy), TLS automático, rate limiting, validação/sanitização de uploads SVG (se habilitar), e monitoramento/log centralizado.

---

## Arquivos-chave

- `main.py` — entrada da aplicação
- `App/__init__.py` — criação do Flask app
- `App/routes.py` — rotas
- `App/static/` — assets JS/CSS
- `Dockerfile`, `compose.yaml` — build/runtimes
- `test-local.ps1` — smoke test PowerShell

---

Faça `.	est-local.ps1` (PowerShell) ou use os `curl`/`Invoke-RestMethod` mostrados para validar localmente.
