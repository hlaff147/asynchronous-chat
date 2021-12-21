# asynchronous-chat

## Imagens, Vídeos e Áudios

Nosso chat faz transferência de dados de arquivos sem restrição quanto ao tipo, mas apenas realiza a visualização de alguns. Até agora, testamos com sucesso visualizações de arquivos tipo mp4, wav e jpg. Mas é fácil testar outros tipos.

Da linha 15 a 17 de `window.py`, são criadas três variáveis de lista, `SUPPORTED_VIDEO_FORMATS `, `SUPPORTED_AUDIO_FORMATS ` e `SUPPORTED_IMAGE_FORMATS `. Para testar um formato diferente, basta incluir a extensão desse tipo de formato na lista do tipo de arquivo.

Por exemplo, para habilitar a visualização de arquivos de imagem png, basta mudar o código de:
   ```python
    SUPPORTED_IMAGE_FORMATS = ['jpg']
   ```
para:
   ```python
    SUPPORTED_IMAGE_FORMATS = ['jpg', 'png']
   ```
Porém, é importante saber que a visualização pode não funcionar com qualquer tipo de arquivo

## Instalação

É preciso instalar os pacotes em `requirements.txt`, o que pode ser feito executando o comando:

```bash
pip install -r requirements.txt
```

Em algumas distribuições de Linux, como Ubuntu e Mint, pode ser necessário instalar outros pacotes com um comando semelhante a:

```bash
sudo apt install python3-tk python3-tk.pillow
```

## Execução

O ponto de entrada para a execução do código é o arquivo `window.py`. Então, você deve usar um dos comandos abaixo:

```bash
python window.py
python3 window.py
```

## Grupo

- Azemar Teixeira (artn)
- Denílson da Silva (dfs9)
- Flávio Braga (fbsj)
- Humber Filho (hlaff)
- João Sobral (jfmvs)
- Lucas Asafe (lavn)
- Sérgio Barreto (slbp)
- Yuri Valença (yvc)
