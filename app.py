from flask import Flask, render_template, request, jsonify
import yt_dlp
import threading

app = Flask(__name__)

# Variável global para armazenar o progresso
progress = {
    'status': '',
    'percent': 0
}

@app.route("/")
def home():
    return render_template("index.html")

# Função que faz o download do áudio e atualiza o progresso
def download_audio(link):
    global progress
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],  # Hook para acompanhar o progresso
        'ffmpeg_location': r'C:\Program Files\ffmpeg\bin',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        progress['status'] = 'done'
    except Exception as e:
        progress['status'] = f'error: {e}'

# Função que faz o download do vídeo e atualiza o progresso
def download_video(link):
    global progress
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],  # Hook para acompanhar o progresso
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        progress['status'] = 'done'
    except Exception as e:
        progress['status'] = f'error: {e}'

# Função chamada pelo yt-dlp para atualizar o progresso
def progress_hook(d):
    global progress
    if d['status'] == 'downloading':
        # Apenas mantenha a porcentagem, removendo sequências de escape
        progress['percent'] = d['_percent_str'].replace('\x1b[0;94m', '').replace('\x1b[0m', '').strip()
    if d['status'] == 'finished':
        progress['status'] = 'done'

@app.route('/mp3', methods=['POST'])
def mp3():
    global progress
    data = request.get_json()
    link = data.get('link')

    # Reseta o progresso
    progress = {'status': 'downloading', 'percent': '0%'}
    
    # Inicia o download em uma thread separada para não bloquear a resposta
    threading.Thread(target=download_audio, args=(link,)).start()

    return jsonify({"status": "Download iniciado"}), 200

@app.route('/mp4', methods=['POST'])
def mp4():
    global progress
    data = request.get_json()
    link = data.get('link')

    # Reseta o progresso
    progress = {'status': 'downloading', 'percent': '0%'}
    
    # Inicia o download em uma thread separada para não bloquear a resposta
    threading.Thread(target=download_video, args=(link,)).start()

    return jsonify({"status": "Download iniciado"}), 200

@app.route('/progress')
def get_progress():
    global progress
    return jsonify(progress), 200

if __name__ == '__main__':
    app.run(debug=True)
