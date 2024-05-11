# controle
# Regras para Colaboração
- Todos os MRs de alteração inicialmente devem ser enviados para a branch develop;
- MRs para branch main devem ser feitas a partir da develop e somente executados ao finalizar uma versão nova;
- Apos merge da develop para main, deve-se gerar uma versão nova da aplicação (Pode pedir pra @MarnieGrenat caso esteja muito ocupado);
- Evite autorizar o próprio MR;
- Documente todas as alterações em *issues* para termos controle das alterações;
- Tente dividir para conquistar as tarefas, para que outros desenvolvedores possam te ajudar a finalizar a issue mais rápido.
  
# Como rodar a aplicação
## Caso não tenha python instalado


instalar git https://git-scm.com/downloads

abrir o programa powershell

rodar o seguinte comando:

```
git clone https://github.com/Doguinhoo/controle

cd controle
```

abrir mais um powershell

no primeiro usar o comando:

```
./src/voluntarios-entrada.exe
```

no segunto usar o comando:

```
./src/voluntarios-saida.exe
```

## Caso pretenda usar python

instalar python https://www.python.org/downloads/

instalar git https://git-scm.com/downloads

abrir o programa powershell

rodar os seguintes comandos na raiz do projeto:

```
pip install -r requirements.txt

git clone https://github.com/Doguinhoo/controle
```
abrir mais um powershell

no primeiro usar o comando:

```
python src/voluntarios-entrada.py
```

no segunto usar o comando:

```
python src/voluntarios-saida.py
```