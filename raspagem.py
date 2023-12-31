#Importando a biblioteca pandas e matplotlib
import pandas as pd
import matplotlib as plt


# Aumentando o número de colunas que o pandas mostra
pd.options.display.max_columns = 20


# Lendo o arquivo .ndjson. Importante: o parâmetro lines=True é necessário para que o pandas consiga ler o arquivo.
# Isso é específico para arquivos .ndjson
jhonata= pd.read_json('zeeschuimer-export-instagram.com-2023-08-21T120135.ndjson', lines=True)


# A variável que eu quero analisar é a 'data'. Vamos transformá-la em um dataframe.
# A variável data é um dicionário, então precisamos usar o método json_normalize para transformá-la em um dataframe.
jhonata = pd.json_normalize(jhonata['data'])


print(jhonata.columns)


# Como podemos ver, temos muitas colunas. Vamos selecionar apenas as que nos interessam.
colunas_desejadas = ['id', 'like_count', 'comment_count', 'user.username',
                    'user.full_name', 'user.is_verified', 'caption.text',
                    'caption.created_at', 'play_count', 'video_duration',
                    'code']
jhonata = jhonata[colunas_desejadas]


# Consertando a coluna 'caption.created_at'
jhonata['caption.created_at'] = jhonata['caption.created_at'].apply(lambda x: pd.Timestamp(x, unit='s'))


# Vamos filtrar apenas os posts com mais de 100.000 likes
jhonata = jhonata[jhonata['like_count'] > 100_000]


# Legal. Qual será o post com mais likes do nosso dataset?
print(
   f"Post com mais likes: \n{jhonata.sort_values(by='like_count', ascending=False).head(1)[['code', 'caption.created_at', 'like_count']]}\n\n")


# E o post com mais comentários?
print(
   f"Post com mais comentários: \n{jhonata.sort_values(by='comment_count', ascending=False).head(1)[['code', 'caption.created_at', 'comment_count']]}\n\n")


# E o post com mais visualizações?
print(
   f"Post com mais views: \n{jhonata.sort_values(by='play_count', ascending=False).head(1)[['code', 'caption.created_at', 'play_count']]}\n\n")


# Qual a média de likes por post?
print(f"Média de likes por post: {jhonata['like_count'].mean()}\n\n")


# Qual a média de comentários por post?
print(f"Média de comentários por post: {jhonata['comment_count'].mean()}\n\n")


# Plotando um lineplot com a quantidade de likes por dia
plt.plot(jhonata['caption.created_at'], jhonata['like_count'])
plt.title('Quantidade de likes por dia/post')
plt.xlabel('Data')
plt.ylabel('Quantidade de likes')
plt.show()
