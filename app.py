import streamlit as st
import re
from datetime import datetime

def validar_numero_cartao(numero):
    """Algoritmo de Luhn para validar número do cartão"""
    # Remove espaços e hífens
    numero = re.sub(r'[^0-9]', '', numero)
    
    # Verifica se tem apenas números e comprimento válido
    if not numero.isdigit() or len(numero) < 13 or len(numero) > 19:
        return False
    
    # Algoritmo de Luhn
    total = 0
    reverse_digits = numero[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Posições ímpares (da direita para esquerda)
            n *= 2
            if n > 9:
                n = (n // 10) + (n % 10)
        total += n
    
    return total % 10 == 0

def validar_validade(validade):
    """Valida se a data está no formato MM/AA e não expirou"""
    try:
        mes, ano = validade.split('/')
        if len(mes) != 2 or len(ano) != 2:
            return False
        
        mes = int(mes)
        ano = int('20' + ano)  # Converte AA para 20AA
        
        if mes < 1 or mes > 12:
            return False
        
        # Verifica se não expirou
        hoje = datetime.now()
        if ano < hoje.year or (ano == hoje.year and mes < hoje.month):
            return False
        
        return True
    except:
        return False

def validar_cvv(cvv):
    """Valida se o CVV tem 3 ou 4 dígitos"""
    return cvv.isdigit() and len(cvv) in [3, 4]

def salvar_dados_cartao(numero, validade, cvv):
    """Salva os dados do cartão em um arquivo txt"""
    with open('cartao_validado.txt', 'w') as arquivo:
        arquivo.write(f"Número do Cartão: {numero}\n")
        arquivo.write(f"Validade: {validade}\n")
        arquivo.write(f"CVV: {cvv}\n")
        arquivo.write(f"Data de Verificação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

# Interface Streamlit
st.title("🔒 Verificador de Cartão de Crédito")

# Mensagem de conscientização
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

# Campos de entrada
st.subheader("📝 Digite os dados do cartão:")

numero_cartao = st.text_input(
    "Número do Cartão de Crédito:", 
    placeholder="1234 5678 9012 3456",
    help="Digite apenas números (espaços serão removidos automaticamente)"
)

validade = st.text_input(
    "Validade do Cartão (MM/AA):", 
    placeholder="12/25",
    help="Formato: MM/AA (exemplo: 12/25)"
)

cvv = st.text_input(
    "Código de Segurança (CVV):", 
    placeholder="123",
    type="password",
    help="3 ou 4 dígitos no verso do cartão"
)

# Botão de verificação
if st.button("🔍 Verificar Cartão de Crédito", type="primary"):
    if numero_cartao and validade and cvv:
        # Validações
        numero_valido = validar_numero_cartao(numero_cartao)
        validade_valida = validar_validade(validade)
        cvv_valido = validar_cvv(cvv)
        
        if numero_valido and validade_valida and cvv_valido:
            st.success("✅ **CARTÃO VÁLIDO!** Todos os dados estão corretos.")
            
            # Salva os dados em arquivo
            try:
                salvar_dados_cartao(numero_cartao, validade, cvv)
                st.info("📄 Dados salvos no arquivo 'cartao_validado.txt'")
            except Exception as e:
                st.error(f"Erro ao salvar arquivo: {e}")
                
        else:
            st.error("❌ **CARTÃO INVÁLIDO!**")
            
            # Mostra erros específicos
            if not numero_valido:
                st.error("• Número do cartão inválido")
            if not validade_valida:
                st.error("• Data de validade inválida ou expirada")
            if not cvv_valido:
                st.error("• CVV deve ter 3 ou 4 dígitos")
    else:
        st.warning("⚠️ Por favor, preencha todos os campos!")

# Rodapé
st.markdown("---")
st.caption("🔐 Sistema educacional - Mantenha seus dados seguros!")