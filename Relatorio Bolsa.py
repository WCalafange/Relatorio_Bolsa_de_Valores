# Código feito por Wesley Calafange em 09/23

# Importação dos módulos que serão utilizados
import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Definindo os codigos dos ativos que serão analisados de acordo com o site da Yahoo Finance
ativos = ["^BVSP", "BRL=X"]

# Definindo as data onde serão coletados os dados
hoje = datetime.datetime.now()
um_ano_atras = hoje - datetime.timedelta(days=365)

# Selecionando e limpandos os dados
dados_mercado = yf.download(ativos, um_ano_atras, hoje)
fechamento_diario = dados_mercado['Adj Close']
fechamento_diario.columns = ['Dólar', 'Bovespa']
fechamento_diario = fechamento_diario.dropna()


# Criando tabelas com outros timeframes
fechamento_mensal = fechamento_diario.resample("M").last()
fechamento_anual = fechamento_diario.resample("Y").last()

# Calculando o retorno diario, mensal e anual
retorno_anual = fechamento_anual.pct_change().dropna()
retorno_mensal = fechamento_mensal.pct_change().dropna()
retorno_diario = fechamento_diario.pct_change().dropna()

retorno_dia_dolar = retorno_diario.iloc[-1, 0]
retorno_dia_bovespa = retorno_diario.iloc[-1, 1]

retorno_mes_dolar = retorno_mensal.iloc[-1, 0]
retorno_mes_bovespa = retorno_mensal.iloc[-1, 1]

retorno_ano_dolar = retorno_anual.iloc[-1, 0]
retorno_ano_bovespa = retorno_anual.iloc[-1, 1]

# Arredondando os valores dos retornos


def arredonda_perc(retorno):
    valor_arredondado = round(retorno*100, 2)
    return valor_arredondado


retorno_dia_dolar = arredonda_perc(retorno_dia_dolar)
retorno_dia_bovespa = arredonda_perc(retorno_dia_bovespa)

retorno_mes_dolar = arredonda_perc(retorno_mes_dolar)
retorno_mes_bovespa = arredonda_perc(retorno_mes_bovespa)

retorno_ano_dolar = arredonda_perc(retorno_ano_dolar)
retorno_ano_bovespa = arredonda_perc(retorno_ano_bovespa)


# Função para criar os gráficos
def gera_grafico(ativo, titulo, nome_arquivo):
    plt.style.use('cyberpunk')
    fechamento_diario.plot(y=ativo, use_index=True, legend=False)

    plt.title(titulo)
    plt.savefig(nome_arquivo, dpi=300)
    plt.show()


# Criando gráfico do Ibovespa
ativo = 'Bovespa'
titulo = 'Indice do Bovespa'
nome_arquivo = 'Ibovespa.png'
gera_grafico(ativo, titulo, nome_arquivo)

# Criando o grafico do Dolar
ativo = 'Dólar'
titulo = 'Cotação do Dólar'
nome_arquivo = 'Dólar.png'
gera_grafico(ativo, titulo, nome_arquivo)

# Configurando o envio do email
load_dotenv()

senha = os.environ.get('senha')
email = 'wesley.calafange@gmail.com'

msg = EmailMessage()
msg['Subject'] = "Relatório diário do Dolar e Ibovespa"
msg['From'] = 'wesley.calafange@gmail.com'
msg['To'] = 'welberk87@gmail.com'

msg.set_content(f'''Prezada Super, segue o relatório diário:

Bolsa:

No ano o Ibovespa está tendo uma rentabilidade de {retorno_ano_bovespa}%, 
enquanto no mês a rentabilidade é de {retorno_mes_bovespa}%.

No último dia útil, o fechamento do Ibovespa foi de {retorno_dia_bovespa}%.

Dólar:

No ano o Dólar está tendo uma rentabilidade de {retorno_ano_dolar}%, 
enquanto no mês a rentabilidade é de {retorno_mes_dolar}%.

No último dia útil, o fechamento do Dólar foi de {retorno_dia_dolar}%.

''')

with open('Dólar.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application',
                       subtype='png', filename='dolar.png')


with open('Ibovespa.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application',
                       subtype='png', filename='ibovespa.png')
# Enviando o email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email, senha)
    smtp.send_message(msg)


print('fim da execução')
