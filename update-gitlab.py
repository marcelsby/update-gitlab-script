#! /usr/bin/env zxpy
import requests

url = "https://hub.docker.com/v2/repositories/gitlab/gitlab-ce/tags"
response = requests.get(url, {"page": 1})

if response.status_code != 200:
    print(f"Falha ao buscar as Tags.")
    print(f"URL requisitada: {response.url}")
    print(f"Status code recebido: {response.status_code}")
    exit(1)

gitlab_tags = None

if response.headers.get("content-type") != "application/json":
    print("A resposta da requisição é um JSON inválido. Não foi possível atualizar o Gitlab.")
    exit(1)

gitlab_tags = response.json()

latest_gitlab_tag = [tag for tag in gitlab_tags["results"] if tag["name"] == "latest"][0]

current_gitlab_digest = str(~'docker inspect --format \'{{.Image}}\' --type container gitlab').strip()

print(f"Current: {current_gitlab_digest}")
print(f"Latest: {latest_gitlab_tag['digest']}")
print(current_gitlab_digest == latest_gitlab_tag['digest'])

# if current_gitlab_digest == latest_gitlab_tag["digest"]:
#     print("Seu Gitlab está atualizado!")
#     print(f"Digest: {current_gitlab_digest}")
#     exit(0)
# else:
#     print("Seu Gitlab precisa ser atualizado!")
#     print("Atualizando...")
    
#     print("Derrubando o contêiner atual e apagando sua imagem...")
#     ~'docker compose down gitlab'

#     print(f"Baixando a imagem mais atualizada. Digest: {latest_gitlab_tag['digest']}")
#     ~'docker compose pull --policy \'always\' gitlab'

#     print("Subindo o serviço novamente com a nova imagem...")
#     ~'docker compose up -d gitlab'