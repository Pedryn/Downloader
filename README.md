## Downloader

Este é um simples script em Python que permite baixar vídeos do YouTube utilizando a biblioteca yt_dlp.

## Como Funciona:

1. Na página o usuário insere o link do vídeo do YouTube que deseja baixar no campo de link.
2. Em seguida, o usuário escolhe entre as opções de download: MP3 (somente áudio) ou MP4 (vídeo completo).
3. Ao selecionar a opção desejada, o frontend envia uma requisição POST para o servidor Flask com o link do vídeo.
4. O servidor Flask recebe a requisição e cria uma instância do yt-dlp, uma biblioteca responsável por baixar o conteúdo do YouTube. Dependendo da escolha do usuário, ele define as configurações para baixar somente o áudio (MP3) ou o vídeo completo (MP4).
5. O download é executado em segundo plano (usando threads) para evitar que a interface do usuário trave enquanto o conteúdo está sendo baixado.
6. O progresso do download é monitorado em tempo real por meio de um "hook" que atualiza a porcentagem de download.
7. O frontend verifica continuamente o progresso, fazendo requisições ao servidor para obter o status do download e atualizando a barra de progresso na página.
8. Assim que o download é concluído, o frontend é notificado e exibe uma mensagem de sucesso ao usuário.
9. Caso ocorra algum erro durante o download, o sistema alerta o usuário sobre o problema.

## Como Usar:

1. Certifique-se de ter o Python instalado em seu sistema.
2. Instale a biblioteca yt_dlp utilizando o seguinte comando: pip install yt_dlp
3. Baixe o ffmpeg caso não possua para rodar o código.
4. Instale o flask com o comando: pip install flask

4. Rode a aplicação flask com `.\env\Scripts\Activate` depois `flask run`.
5. Quando solicitado, insira o link do vídeo do YouTube que deseja baixar.
6. Aguarde até que o download seja concluído e verifique o diretório onde o script está localizado para encontrar o vídeo baixado.

## Observações:

- Este script atualmente suporta apenas o download de vídeos no formato MP4 e audio MP3.