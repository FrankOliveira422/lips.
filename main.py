import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio

# Função para escolher o diretório de destino
def escolher_diretorio():
    diretorio = filedialog.askdirectory()
    if diretorio:
        diretorio_var.set(diretorio)

# Função para baixar o vídeo ou áudio com base nas opções selecionadas
def baixar_video_audio():
    # Obtenha o link do vídeo a partir da entrada
    link = entrada_link.get()

    # Obtenha o formato selecionado (MP3 ou MP4)
    formato = formato_var.get()

    # Obtenha a qualidade selecionada
    qualidade = qualidade_var.get()

    # Obtenha o diretório de destino
    diretorio_destino = diretorio_var.get()

    # Verifique se a opção selecionada é "Áudio (MP3)"
    if formato == "MP3":
        # Baixe o vídeo
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).first()
        video_title = yt.title
        stream.download(output_path=diretorio_destino)
        
        # Converta o áudio para MP3
        input_file = f"{diretorio_destino}/{video_title}.webm"
        output_file = f"{diretorio_destino}/{video_title}.mp3"
        ffmpeg_extract_audio(input_file, output_file)
        
        print(f"Áudio (MP3) baixado e convertido com sucesso: {output_file}")

    else:
        # Baixe o vídeo (MP4)
        yt = YouTube(link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=qualidade).first()
        stream.download(output_path=diretorio_destino)
        
        print(f"Vídeo (MP4) baixado com sucesso: {yt.title}.mp4")

# Crie uma janela
janela = tk.Tk()
janela.title("LIPS - Baixador de Vídeos e Músicas")
janela.geometry("400x400")  # Defina o tamanho da janela

# Defina as cores de fundo e de texto
cor_fundo = "#FFFFFF"  # Branco
cor_texto = "#333333"  # Cinza escuro
cor_botao = "#4287f5"  # Azul claro

# Defina o fundo da janela e o texto
janela.configure(bg=cor_fundo)

# Estilo para o Radiobutton e Combobox
estilo = ttk.Style()
estilo.configure('TButton', background=cor_fundo)
estilo.configure('TRadiobutton', background=cor_fundo)
estilo.configure('TCombobox', background=cor_fundo)

# Adicione um rótulo para destacar o nome "LIPS"
rotulo_nome = tk.Label(janela, text="LIPS", font=("Helvetica", 24), bg=cor_fundo, fg=cor_botao)
rotulo_nome.pack(pady=10)

# Crie uma entrada de texto
entrada_link = tk.Entry(janela, width=40, bg=cor_fundo, fg=cor_texto)
entrada_link.pack(padx=10, pady=10)

# Opção para escolher o formato (MP3, MP4)
formato_var = tk.StringVar()
formato_var.set("MP4")  # Defina o formato padrão
formato_frame = ttk.Frame(janela, padding=(10, 5))
formato_frame.pack()
formato_label = tk.Label(formato_frame, text="Formato:", bg=cor_fundo, fg=cor_texto)
formato_label.pack(side="left")
formato_mp3 = ttk.Radiobutton(formato_frame, text="Áudio (MP3)", variable=formato_var, value="MP3")
formato_mp3.pack(side="left", padx=5)
formato_mp4 = ttk.Radiobutton(formato_frame, text="Vídeo (MP4)", variable=formato_var, value="MP4")
formato_mp4.pack(side="left")

# Opção para escolher a qualidade do vídeo
qualidade_var = tk.StringVar()
qualidade_var.set("720p")  # Defina a qualidade padrão
qualidade_frame = ttk.Frame(janela, padding=(10, 5))
qualidade_frame.pack()
qualidade_label = tk.Label(qualidade_frame, text="Qualidade:", bg=cor_fundo, fg=cor_texto)
qualidade_label.pack(side="left")
qualidade_combobox = ttk.Combobox(qualidade_frame, textvariable=qualidade_var, values=["720p", "1080p", "4K"], state="readonly")
qualidade_combobox.pack(side="left", padx=5)
qualidade_combobox.set("720p")  # Defina a qualidade padrão

# Botão para escolher o diretório de destino
diretorio_var = tk.StringVar()
diretorio_var.set("")  # Inicialmente, nenhum diretório selecionado
escolher_diretorio_btn = tk.Button(janela, text="Escolher Diretório de Destino", command=escolher_diretorio, bg=cor_botao, fg=cor_fundo)
escolher_diretorio_btn.pack(pady=10)

# Exiba o diretório selecionado
diretorio_label = tk.Label(janela, textvariable=diretorio_var, bg=cor_fundo, fg=cor_texto)
diretorio_label.pack(pady=5)

# Botão para baixar o vídeo ou áudio
botao_download = tk.Button(janela, text="Baixar Vídeo/Música", command=baixar_video_audio, bg=cor_botao, fg=cor_fundo)
botao_download.pack(pady=10)

# Inicie o loop principal da interface gráfica
janela.mainloop()
