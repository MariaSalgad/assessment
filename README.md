# COMO RODAR O PROJETO

Para fazer o projeto rodar, é necessário que se possua um banco MySQL instalado na máquina, caso não possua, pode ser baixado [aqui](https://www.apachefriends.org/download.html)

Feito isso, deve-se criar um banco com o nome de "teste" ou editar no servidor.py o nome do banco de dados.

Com isso, pode rodar o arquivo servidor.py e logo após o client.py.

O client.py enviará uma mensagem a cada 1 segundo para o servidor, e a mensagem será tratada e salva conforme os parâmetros no banco de dados.