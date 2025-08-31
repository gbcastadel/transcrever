import streamlit as st
import whisper
from transformers import pipeline
import os

# Função para transcrever o áudio
def transcrever_audio(caminho_audio):
    modelo = whisper.load_model("small")
    resultado = modelo.transcribe(caminho_audio, language="pt")
    segmentos = resultado["segments"]

    texto_segmentado = []
    for seg in segmentos:
        inicio = seg["start"]
        fim = seg["end"]
        texto = seg["text"]
        texto_segmentado.append(f"({inicio:.2f}s - {fim:.2f}s): {texto}")

    return "\n".join(texto_segmentado)

# Função para salvar arquivos
def salvar_arquivo(conteudo, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)

# Interface Streamlit
st.title("🎙 Transcrição de Áudio")
st.write("Envie um arquivo de áudio em Português para transcrição automática.")

arquivo_audio = st.file_uploader("📤 Upload do arquivo de áudio", type=["mp3", "wav", "m4a"])

if arquivo_audio is not None:
    caminho_temporario = "temp_audio." + arquivo_audio.name.split('.')[-1]
    
    # Salva o arquivo temporariamente
    with open(caminho_temporario, "wb") as f:
        f.write(arquivo_audio.read())

    with st.spinner("🔍 Processando o áudio..."):
        texto = transcrever_audio(caminho_temporario)


    st.success("✅ Transcrição e resumo concluídos!")
    st.subheader("📝 Transcrição")
    st.text_area("Texto transcrito", texto, height=300)

    # Botões para salvar os arquivos
    if st.button("💾 Salvar Transcrição"):
        salvar_arquivo(texto, "transcricao.txt")
        st.success("Transcrição salva como 'transcricao.txt'")

    # Limpeza do arquivo temporário
    os.remove(caminho_temporario)