# 🔒 Verificador de Cartão de Crédito

Sistema simples e educacional para validação de dados de cartão de crédito usando Python e Streamlit.

## 📋 Funcionalidades

- ✅ Validação de número do cartão (Algoritmo de Luhn)
- ✅ Verificação de data de validade (MM/AA)
- ✅ Validação do código CVV (3 ou 4 dígitos)
- ✅ Interface web amigável
- ✅ Mensagens de conscientização sobre segurança
- ✅ Salvamento de dados válidos em arquivo .txt

## 🚀 Como Usar

### 1. Pré-requisitos

```bash
Python 3.7 ou superior
```

### 2. Instalação

```bash
# Clone ou baixe o arquivo
# Instale as dependências
pip install streamlit
```

### 3. Executar o Programa

```bash
streamlit run app.py
```

### 4. Acessar a Aplicação

Abra seu navegador em: `http://localhost:8501`

## 📝 Como Funciona

1. **Digite o número do cartão** (apenas números)
2. **Informe a validade** no formato MM/AA
3. **Digite o CVV** (3 ou 4 dígitos)
4. **Clique em "Verificar"**
5. Se válido, os dados são salvos em `cartao_validado.txt`

## 🔐 Validações Implementadas

### Número do Cartão
- Algoritmo de Luhn para verificação matemática
- Aceita cartões de 13 a 19 dígitos
- Remove automaticamente espaços e hífens

### Data de Validade
- Formato obrigatório: MM/AA
- Verifica se a data não expirou
- Valida mês (01-12)

### CVV
- Aceita 3 ou 4 dígitos
- Apenas números

## ⚠️ Importante

**Este sistema é apenas para fins educacionais!**

- Nunca use dados reais de cartão
- Não compartilhe informações financeiras
- Mantenha seus dados seguros

## 📁 Estrutura de Arquivos

```
projeto/
│
├── verificador_cartao.py    # Código principal
├── README.md               # Este arquivo
└── cartao_validado.txt     # Gerado após validação (se válido)
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit** - Interface web
- **Datetime** - Validação de datas
- **Re** - Expressões regulares

## 📄 Exemplo de Uso

**Dados de teste (fictícios):**
- Número: `4532 1488 0343 6467`
- Validade: `12/25`
- CVV: `123`

## 🤝 Contribuição

Este é um projeto educacional. Sugestões de melhorias são bem-vindas!

## 📜 Licença

Projeto de uso livre para fins educacionais.

---

**🔐 Lembre-se: Proteja sempre seus dados financeiros!**