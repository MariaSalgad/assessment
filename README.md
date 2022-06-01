# COMO RODAR O PROJETO

Para fazer o projeto rodar, é necessário que se possua um banco MySQL e servidor instalado na máquina, caso não possua, pode ser baixado [aqui](https://www.apachefriends.org/download.html) (O link é do pacote Xampp, onde facilita a instalação, bem como, possui servidor Apache e conseguimos ver o banco de dados graficamente).

Feito isso, deve-se criar um banco com o nome de "teste" ou editar no servidor.py o nome do banco de dados.

Com isso, pode rodar o arquivo servidor.py e logo após o client.py.

O client.py enviará uma mensagem a cada 1 segundo para o servidor, a mensagem será tratada e salva conforme os parâmetros no banco de dados. Para encerrar a aplicação do client.py é necessário apenas pressionar a tecla Enter.