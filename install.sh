#!/bin/bash

### Script de instalação do software Troca-HD

function InstalaDependecias()
{

if [ $USER = "root" ]

then

	echo '
Instalando dependências.
'
	apt update && apt upgrade -y && apt install python3 python3-dev python3-pil python3-tk tk tk-dev python3-pip libpng12-dev libfreetype6-dev libblas-dev liblapack-dev && pip3 install numpy scipy openpyxl matplotlib

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
chmod +x trocahd_oop.py

cd menu
sed -i "s|MYSOFTPATH|$MYPATH|g" frmenu.py
cd ..

}

function CriaDesktop()
{

echo '
Criando atalho de inicialização do programa - arquivo: troca-hd.desktop
'

EXECPATH="$MYPATH/trocahd_oop.py"
sed -i "s|TROCAHDEXECPATH|$EXECPATH|g" troca-hd.desktop

ICONPATH="$MYPATH/Calculator.png"
sed -i "s|TROCAHDICONPATH|$ICONPATH|g" troca-hd.desktop

chmod +x troca-hd.desktop

if [ $USER = 'root' ]

then

	mv troca-hd.desktop /usr/share/applications/

else

	mv troca-hd.desktop ~/.local/share/applications/

fi

}

echo '
***********************Aplicativo de instalação Troca-HD!***********************
'

sleep 5

InstalaDependecias

CorrigeCaminhos

CriaDesktop
