# troca-hd

Dependências: python3 (testado em python 3.5.1+ Ubuntu 16.04), numpy, scipy, tk (tkinter), openpyxl (futuramente tk-dev e matplolib)

Instalação:

	1) Descompactar o arquivo .tar.xz ou clonar o diretório no github (git clone https://github.com/vicerodrigues/troca-hd.git)

	2) Tornar o script de instalação executável (chmod +x install.sh)

	3) Executar o script de instalação. Caso este seja executado como root irá automaticamente atualizar o sistema e instalar as dependências, sendo o arquivo de atalho (.desktop) encaminhado para a pasta /usr/share/applications. Caso não seja executado como root o arquivo de atalho irá para a pasta ~/.local/share/applications

Desinstalação:

	1) O único arquivo criado fora da pasta do programa é o arquivo de atalho troca-hd.desktop que deve ser excluído manualmente.