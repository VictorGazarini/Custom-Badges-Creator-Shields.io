<p align="center">
	<img src="https://img.shields.io/badge/Badge-Creator-blue?style=flat&labelColor=%23ffffff&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48IS0tIFVwbG9hZGVkIHRvOiBTVkcgUmVwbywgd3d3LnN2Z3JlcG8uY29tLCBHZW5lcmF0b3I6IFNWRyBSZXBvIE1peGVyIFRvb2xzIC0tPg0KPHN2ZyB3aWR0aD0iODAwcHgiIGhlaWdodD0iODAwcHgiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4NCjxwYXRoIGQ9Ik0xMSAwTDE2IDVMMTQgN1YxMkwzIDE2TDIuMjA3MTEgMTUuMjA3MUw2LjQ4MTk2IDEwLjkzMjNDNi42NDcxOCAxMC45NzY0IDYuODIwODQgMTEgNyAxMUM4LjEwNDU3IDExIDkgMTAuMTA0NiA5IDlDOSA3Ljg5NTQzIDguMTA0NTcgNyA3IDdDNS44OTU0MyA3IDUgNy44OTU0MyA1IDlDNSA5LjE3OTE2IDUuMDIzNTYgOS4zNTI4MiA1LjA2Nzc0IDkuNTE4MDRMMC43OTI4OTMgMTMuNzkyOUwwIDEzTDQgMkg5TDExIDBaIiBmaWxsPSIjMDAwMDAwIi8%2BDQo8L3N2Zz4%3D" alt="Badge Preview" width="800" />
</p>

<p align="center">
	<img src="https://img.shields.io/badge/license-MIT-green?style=flat" alt="MIT License" width="150" />
	<img src="https://img.shields.io/badge/docker-ready-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker Ready" width="200" />
	<img src="https://img.shields.io/badge/community-open%20source-blue?style=flat" alt="Open Source" width="290" />
</p>

# Custom Shields.io Badge Creator

Aplicação Flask para gerar URLs de badges do Shields.io com interface web e API JSON.

## Visão geral 

- O projeto foi desenvolvido para possibilitar a criação de badges de forma interativa e dinâmica.
- O núcleo da aplicação é o conversor customizável de SVG, usado para transformar uploads em badges ou recursos visuais reutilizáveis.
- Backend: Flask.
- Frontend: HTML + JavaScript + Tailwind CSS.
- Execução: local ou via Docker.
- Estado: a aplicação é stateless, então não depende de banco de dados.

## Estrutura

- `main.py` inicializa o servidor.
- `App/__init__.py` cria a aplicação Flask e configura headers de segurança.
- `App/routes.py` expõe as rotas da UI e da API.
- `App/templates/index.html` contém a interface principal.
- `App/static/` contém JS e CSS gerado pelo Tailwind.
- O fluxo de SVG é tratado no frontend e servido pela API para manter a experiência interativa.

## Rotas

- `GET /` - página web.
- `GET /api/healthz` - health check.
- `POST /api/generate` - gera a URL do badge a partir de JSON.

## Exemplos de uso da API

Health check:

```bash
curl http://localhost:5000/api/healthz
```

Gerar badge com `curl`:

```bash
curl -X POST http://localhost:5000/api/generate \
	-H "Content-Type: application/json" \
	-d '{"label":"BUILD","message":"PASSING","color":"brightgreen","style":"flat","logo":"github"}'
```

Exemplo em PowerShell:

```powershell
$body = @{ label='BUILD'; message='PASSING'; color='brightgreen'; style='flat'; logo='github' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:5000/api/generate" -ContentType "application/json" -Body $body
```

Resposta esperada:

```json
{"url":"https://img.shields.io/badge/BUILD-PASSING-brightgreen?style=flat&logo=github"}
```

Erros comuns:

```json
{"error":"invalid_json","details":"Send a JSON object body."}
```

Status HTTP: `400 Bad Request`

Quando o campo `message` não é enviado:

```json
{"error":"validation_error","details":"'message' is required"}
```

Status HTTP: `400 Bad Request`

## Pré-requisitos

- Python 3.11+.
- Node.js 18+.
- Docker e Docker Compose, se quiser rodar via container.

## Como rodar localmente com Docker

1. Garanta que o Docker Desktop ou Docker Engine esteja ativo.
2. No diretório do projeto, rode:

```bash
docker compose up -d --build
```

3. Abra no navegador:

```text
http://localhost:5000
```

4. Para parar:

```bash
docker compose down
```

## Desenvolvimento local sem Docker

Se quiser rodar direto no Python:

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
npm install
npm run build:css
python main.py
```

## Observações técnicas

- O projeto usa Tailwind compilado para `App/static/output.css`.
- Se alterar estilos, rode `npm run build:css` antes de rebuildar o container.
- O backend monta a URL final do badge com base em `label`, `message`, `color`, `style` e demais parâmetros opcionais.

## Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE`.

## Contribuindo

Contribuições são bem-vindas. Se quiser ajudar:

1. Faça um fork do repositório.
2. Crie uma branch com sua alteração.
3. Envie um pull request com uma descrição objetiva.

Antes de abrir o PR, verifique se a aplicação sobe corretamente com Docker e se os arquivos estáticos foram recompilados quando necessário.

## Roadmap

- Melhorar a experiência de conversão de SVG.
- Adicionar mais validações de entrada na API.
- Incluir exemplos de uso e screenshots.
- Adicionar redirecionamento de links personalizável.
- Evoluir a pipeline de build e deploy.
