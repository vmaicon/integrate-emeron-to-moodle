# %%
import pandas as pd

def clean_data(df):
    # Alterar o tipo para string
    df['idPessoa'] = df['idPessoa'].astype(str).str.zfill(11)
    return df

# Variável carregada 'df' do URI: /home/maicon/git/esjud/integracao-emeron-moodle/_SELECT_Inscricao_idInscricao_InscricaoAluno_idPessoa_Pessoa_nom_202405201404.csv
df = pd.read_csv(r'dataset/_SELECT_Inscricao_idInscricao_InscricaoAluno_idPessoa_Pessoa_nom_202405201404.csv')

df_clean = clean_data(df.copy())

# %%
def clean_data_mdl_user(df):
    # Filtrar linhas com base na coluna: 'username'
    df = df.set_index('username')
    df = df.filter(regex="(^\\d+)",axis=0)
    return df

# Variável carregada 'df' do URI: /home/maicon/git/esjud/integracao-emeron-moodle/mdl_user.csv
df = pd.read_csv(r'dataset/mdl_user-v2.csv')

df_mdl_user = clean_data_mdl_user(df.copy()).reset_index()


# %%
df_clean['username'] = df_clean['idPessoa']

# %%
df_merged = df_clean.merge(df_mdl_user,on='username', how='outer')

# %%
df_merged.columns

# %% [markdown]
# Faço uma cópia com as colunas ['idPessoa','username','firstname', 'email', 'auth', 'firstaccess] e removo os duplicados
# - com a coluna 'firstaccess' eu consigo ver três situações:
# - não cadastrados no emeron
# - não cadastrados no moodle
# - usuários que nunca acessaram (que estão com valor 0)

# %%
df_analise = df_merged[['idPessoa','username','firstname', 'email', 'auth', 'firstaccess']].copy().drop_duplicates()

# %%
# converte uma nova coluna
df_analise['firstaccess_datetime'] = pd.to_datetime(df_analise['firstaccess'], unit='s', errors='coerce')

# %%
df_analise.columns


# %%
df_analise = df_analise.drop('firstaccess', axis=1)

# %%
df_analise = pd.concat([df_analise, df_merged[['lastaccess','lastlogin']]], axis=1)

# %%
df_analise['lastaccess'] = pd.to_datetime(df_analise['lastaccess'], unit='s', errors='coerce')

# %%
df_analise['lastlogin'] = pd.to_datetime(df_analise['lastlogin'], unit='s', errors='coerce')

# %%
df_merged = df_merged[df_merged['nome.1'].str.contains("Artifi", regex=False, na=False)]

# %%
df_nulos_no_emeron = df_merged[df_merged['idPessoa'].isnull() == True]

# %%
df_nulos_no_emeron


