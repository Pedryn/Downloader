from flask import Flask, render_template, request, jsonify
import yt_dlp
import threading
import instaloader
import os
import time

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

# Função que faz o download de vídeos ou perfis do Instagram
def download_instagram(link):
    global progress
    loader = instaloader.Instaloader()
    loader.save_metadata = False  # Evita criar arquivos .json
    loader.download_video_thumbnails = False  # Não baixa miniaturas de vídeos

    progress['status'] = 'downloading'
    try:
        if "instagram.com" in link:
            shortcode = link.split("/")[-2]  # Extrai o shortcode do link
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            if post.is_video:
                loader.download_post(post, target="downloads")
                progress['status'] = 'done'
            else:
                progress['status'] = 'error: O link fornecido não é de um vídeo.'
        else:
            loader.download_profile(link, profile_pic=False, fast_update=True)
            progress['status'] = 'done'

        # Remoção de arquivos indesejados
        for root, dirs, files in os.walk("downloads"):
            for file in files:
                if file.endswith(".json") or file.endswith(".txt"):
                    os.remove(os.path.join(root, file))
    except Exception as e:
        progress['status'] = f'error: {e}'

# Função chamada pelo yt-dlp para atualizar o progresso
def progress_hook(d):
    global progress
    if d['status'] == 'downloading':
        progress['percent'] = d['_percent_str'].replace('\x1b[0;94m', '').replace('\x1b[0m', '').strip()
    if d['status'] == 'finished':
        progress['status'] = 'done'

@app.route('/mp3', methods=['POST'])
def mp3():
    global progress
    data = request.get_json()
    link = data.get('link')

    progress = {'status': 'downloading', 'percent': '0%'}
    threading.Thread(target=download_audio, args=(link,)).start()

    return jsonify({"status": "Download iniciado"}), 200

@app.route('/mp4', methods=['POST'])
def mp4():
    global progress
    data = request.get_json()
    link = data.get('link')

    if not link:
        return jsonify({"error": "Nenhum link fornecido."}), 400

    progress = {'status': 'downloading', 'percent': '0%'}
    threading.Thread(target=download_mp4, args=(link,)).start()

    return jsonify({"status": "Download de MP4 iniciado"}), 200

def download_mp4(link):
    global progress
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        progress['status'] = 'done'
    except Exception as e:
        progress['status'] = f'error: {e}'



@app.route('/instagram', methods=['POST'])
def instagram():
    global progress
    data = request.get_json()
    link_or_user = data.get('link_or_user')

    if not link_or_user:
        return jsonify({"error": "Nenhum link ou usuário fornecido."}), 400

    progress = {'status': 'downloading', 'percent': '0%'}
    threading.Thread(target=download_instagram, args=(link_or_user,)).start()

    return jsonify({"status": "Download iniciado"}), 200


@app.route('/progress')
def get_progress():
    global progress
    return jsonify(progress), 200

if __name__ == '__main__':
    app.run(debug=True)
