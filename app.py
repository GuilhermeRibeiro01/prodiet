import streamlit as st
import requests
import base64
import os

ENDPOINT_URL = "https://5rotm3ugf5.execute-api.us-east-1.amazonaws.com"

st.title("Upload de documento")

# product_id = st.selectbox("Tipo de seguro", ["Vida", "Automóvel"])
caloric = st.selectbox("Calorias", ["normocalorica", "hipercalorica"])
age = st.selectbox("Idade", ["adulto", "criança"])
unid = st.selectbox("Unidade", ["litro", "grama", "mililitro"])
document_type = st.selectbox("Tipo de Documento", ["txt","pdf", "csv"])

arquivo = st.file_uploader("Escolha um arquivo", type=['txt','pdf', 'csv'])

if arquivo:
    nome_arquivo = os.path.basename(arquivo.name)
    st.write("Nome do arquivo:", nome_arquivo)

    if st.button("Enviar"):
        # Dados para a requisição da URL assinada
        dados_requisicao = {
            "object_key": nome_arquivo,  # Adicionar object_key aqui
            "caloric": caloric,
            "idade": age,
            "unidade": unid,
            "documentType": document_type
        }

        # 1. Obter URL assinada da API (incluindo metadados na requisição)
        url_assinada_resposta = requests.post(
            ENDPOINT_URL + "/product", json=dados_requisicao 
        )

        if url_assinada_resposta.status_code == 200:
            url_assinada = url_assinada_resposta.json().get("uploadURL")

            upload_resposta = requests.put(url_assinada, data=arquivo)

            if upload_resposta.status_code == 200:
                st.success("Arquivo enviado com sucesso!")
            else:
                st.error(f"Erro ao enviar arquivo: {upload_resposta.text}")
        else:
            st.error(f"Erro ao obter URL assinada: {url_assinada_resposta.text}")