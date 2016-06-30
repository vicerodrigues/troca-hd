#!/bin/bash

### Script de instalação do software Troca-HD

function InstalaDependecias()
{

if [ $USER = "root" ]

then

	echo '
Instalando dependências.
'
	apt update && apt upgrade -y && apt install python3 python3-dev python3-pil python3-tk tk tk-dev python3-pip libpng12-dev libfreetype6-dev && pip3 install numpy scipy openpyxl matplotlib

else

	echo '
Dependências não serão instaladas pois o usuário atual não é o root!
'

fi

}

function CorrigeCaminhos()
{

echo '
Atualizando o caminho de instalação no software.
'

MYPATH="$(pwd)"
sed -i "s|MYSOFTPATH|$MYPATH|g" trocahd_oop.py

cd menu
sed -i "s|MYSOFTPATH|$MYPATH|g" frmenu.py

}

function CriaDesktop()
{

echo '
Criando atalho de inicialização do programa - arquivo: troca-hd.desktop

***EM ANDAMENTO***
'

}

echo '***********************Aplicativo de instalação Troca-HD!***********************'

sleep 5

InstalaDependecias

CorrigeCaminhos

CriaDesktop