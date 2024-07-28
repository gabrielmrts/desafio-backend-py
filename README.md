Primeiro renomeie seu `.env.example` para `.env`

A configuração nele já está correta para desenvolvimento, mas fique livre caso queira alterar.

Faça a build da imagem rodando: `docker build -t desafio-py:latest .`

Subindo para desenvolvimento local:
Comandos:
- `./run.sh up`
- `./run.sh tests`
- `./run.sh down`

Os comandos são auto explicativos, a aplicação roda em um container do docker.
Obs:
Para rodar os testes, primeiro rode o up para iniciar o banco de dados, redis e etc..

Rodando com Docker Compose:
Ao executar `./run.sh up`, você vai subir um container local (a imagem precisa estar buildada, veja no inicio),
e aplicação vai está rodando em: `http://localhost:8000`
a documentação você acessa em: `http://localhost:8000/docs`

Deploy com Kubernetes:
As configurações do kubernetes estão feitas, e os arquivos disponíveis.
Caso queira fazer o deploy do projeto, basta buildar a imagem, subir no dockerhub e apontar ela 
dentro do arquivo app-deployment.yaml