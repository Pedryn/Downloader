import instaloader
import os

# Inicializa o instaloader
loader = instaloader.Instaloader()

# Configurações para evitar arquivos adicionais
loader.save_metadata = False  # Evita criar arquivos .json
loader.download_video_thumbnails = False  # Não baixa miniaturas de vídeos

# URL do vídeo ou nome do perfil
url_ou_usuario = input("Digite o nome do perfil ou o link do vídeo: ")

try:
    if "instagram.com" in url_ou_usuario:
        # Extrai o código curto do post do link
        shortcode = url_ou_usuario.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        if post.is_video:
            print("Baixando vídeo...")
            loader.download_post(post, target="downloads")
        else:
            print("O link fornecido não é de um vídeo.")
    else:
        print(f"Baixando vídeos do perfil '{url_ou_usuario}'...")
        loader.download_profile(url_ou_usuario, profile_pic=False, fast_update=True)
except Exception as e:
    print(f"Ocorreu um erro: {e}")

# Remover arquivos indesejados (caso criados)
for root, dirs, files in os.walk("downloads"):
    for file in files:
        if file.endswith(".json") or file.endswith(".txt"):
            os.remove(os.path.join(root, file))
