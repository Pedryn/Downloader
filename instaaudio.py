import instaloader
import os
from moviepy.editor import VideoFileClip

# Inicializa o instaloader
loader = instaloader.Instaloader()

# Configurações do Instaloader
loader.save_metadata = False  # Evita criar arquivos .json
loader.download_video_thumbnails = False  # Não baixa miniaturas de vídeos

# Função para extrair áudio do vídeo
def extract_audio(video_path, output_path):
    try:
        video = VideoFileClip(video_path)
        audio_path = os.path.splitext(output_path)[0] + ".mp3"
        video.audio.write_audiofile(audio_path)
        print(f"Áudio salvo em: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"Erro ao extrair áudio: {e}")

# URL do vídeo
url_ou_usuario = input("Digite o link do vídeo no Instagram: ")

try:
    if "instagram.com" in url_ou_usuario:
        # Extrai o código curto do post do link
        shortcode = url_ou_usuario.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        if post.is_video:
            print("Baixando vídeo...")
            loader.download_post(post, target="downloads")
            
            # Localizar o arquivo de vídeo baixado
            for root, dirs, files in os.walk("downloads"):
                for file in files:
                    if file.endswith(".mp4"):
                        video_path = os.path.join(root, file)
                        print(f"Vídeo baixado em: {video_path}")
                        
                        # Extrair áudio
                        extract_audio(video_path, video_path)
                        
                        # Opcional: Deletar o vídeo após extrair o áudio
                        os.remove(video_path)
        else:
            print("O link fornecido não é de um vídeo.")
    else:
        print("Por favor, forneça um link válido de um vídeo do Instagram.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
