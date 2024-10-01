from pathlib import Path
import streamlit as st
import openai
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv, find_dotenv

# Carrega as variáveis de ambiente do arquivo .env, se houver
_ = load_dotenv(find_dotenv())

# Criação de pastas temporárias para armazenar arquivos de áudio e vídeo
PASTA_TEMP = Path(__file__).parent / 'temp'
PASTA_TEMP.mkdir(exist_ok=True)  # Garante que a pasta "temp" exista
ARQUIVO_AUDIO_TEMP = PASTA_TEMP / 'audio.mp3'
ARQUIVO_VIDEO_TEMP = PASTA_TEMP / 'video.mp4'

# Inicializa o cliente da API da OpenAI
client = openai.OpenAI()

# Função para transcrever áudio utilizando a API da OpenAI
def transcreve_audio(caminho_audio, prompt):
    with open(caminho_audio, 'rb') as arquivo_audio:
        # Envia o arquivo de áudio para a API Whisper da OpenAI para transcrição
        transcricao = client.audio.transcriptions.create(
            model='whisper-1',
            language='pt',  # Define o idioma como português
            response_format='text',
            file=arquivo_audio,
            prompt=prompt,
        )
        return transcricao

# Função para salvar o áudio de um vídeo enviado pelo usuário
def _salva_audio_do_video(video_bytes):
    # Salva o vídeo enviado como arquivo temporário
    with open(ARQUIVO_VIDEO_TEMP, mode='wb') as video_f:
        video_f.write(video_bytes.read())
    # Extrai o áudio do vídeo e salva como arquivo de áudio
    moviepy_video = VideoFileClip(str(ARQUIVO_VIDEO_TEMP))
    moviepy_video.audio.write_audiofile(str(ARQUIVO_AUDIO_TEMP))

# Função para processar o upload de um vídeo e transcrever seu áudio
def transcreve_tab_video():
    # Campo para o usuário inserir um prompt opcional para a transcrição
    prompt_input = st.text_input('(opcional) Digite o seu prompt', key='input_video', placeholder='Aula de biologia')
    # Upload de arquivo de vídeo pelo usuário
    arquivo_video = st.file_uploader('Adicione um arquivo de vídeo .mp4', type=['mp4'])
    
    # Se o arquivo de vídeo for enviado, processa a transcrição
    if not arquivo_video is None:
        _salva_audio_do_video(arquivo_video)  # Extrai o áudio do vídeo
        transcricao = transcreve_audio(ARQUIVO_AUDIO_TEMP, prompt_input)  # Transcreve o áudio
        st.write(transcricao)  # Exibe a transcrição no app

# Função para processar o upload de um arquivo de áudio e transcrevê-lo
def transcreve_tab_audio():
    # Campo para o usuário inserir um prompt opcional para a transcrição
    prompt_input = st.text_input('(opcional) Digite o seu prompt', key='input_audio', placeholder='Aula de biologia')
    # Upload de arquivo de áudio pelo usuário
    arquivo_audio = st.file_uploader('Adicione um arquivo de áudio .mp3', type=['mp3'])
    
    # Se o arquivo de áudio for enviado, processa a transcrição
    if not arquivo_audio is None:
        transcricao = client.audio.transcriptions.create(
            model='whisper-1',
            language='pt',  # Define o idioma como português
            response_format='text',
            file=arquivo_audio,
            prompt=prompt_input
        )
        st.write(transcricao)  # Exibe a transcrição no app

# Função principal que define a estrutura do Streamlit
def main():
    st.header('Bem-vindo ao [Daniel Prazeres](https://danielprazeres.com) Transcript🎙️', divider=True)
    st.markdown('#### Transcreva áudio de vídeos e arquivos de áudio')
    
    # Definição das abas do aplicativo: uma para vídeo e outra para áudio
    tab_video, tab_audio = st.tabs(['Vídeo', 'Áudio'])
    
    # Carrega a aba correspondente
    with tab_video:
        transcreve_tab_video()
    with tab_audio:
        transcreve_tab_audio()

# Execução do aplicativo Streamlit
if __name__ == '__main__':
    main()