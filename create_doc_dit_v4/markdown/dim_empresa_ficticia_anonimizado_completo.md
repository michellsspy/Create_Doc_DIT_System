## Tabela: refined.d_empresas_farol

### Objetivo:
Tabela da dimensão de empresas do indicador farol.

### Fontes de Dados

| Origem                             | Descrição                                  |
|------------------------------------|--------------------------------------------|
|trusted.tb_tab_empresa_farol              | Tabela de empresas.                        |
|raw.sharepoint_dados_filiais_farol        | Tabela do sharepoint com dados de filiais. |
|refined.tb_farol_faturamento_farol        | Tabela com dados de faturamento.           |


### Histórico de alterações

| Data       | Desenvolvido por | Modificações          |
|------------|------------------|-----------------------|
| 22/05/2025 | Michel Santana   | Criação do notebook   |


```python
# Importa e executa o notebook `ingestion_function`, localizado em `../00_config/`.
# 
# O comando `%run` carrega todas as funções, variáveis e configurações definidas no notebook referenciado
# para o ambiente atual. Isso permite reutilizar lógica comum, como funções de ingestão de dados, sem duplicação de código.
# 
# Útil para centralizar rotinas reutilizáveis e manter notebooks modulares e organizados.
```


```python
%run ../00_config/ingestion_function
```


```python
debug = False

container_target = 'camada_destino'
directory = 'diretorio_ficticio'
table_name = 'dim_empresa_ficticia'
delta_table_name = f'{environment}.{container_target}.{table_name}'
delta_file = f"abfss://{container_target}@{nome_datalake_ficticio}.dfs.core.windows.net/{directory}/{table_name}/"
comment_delta_table = 'Tabela de dimensão de empresas fictícias.'

print(f'delta_table_name = {table_name}')
print(f'delta_file = {delta_file}')
```


```python
"""
Cria um widget interativo chamado `reprocessar` para controle da carga da dimensão.

- Exibe um dropdown com as opções "True" e "False".
- A variável `reprocessar` será `True` apenas se o usuário selecionar essa opção no notebook.

Objetivo: permitir que o usuário escolha, de forma interativa, se a carga será completa (`overwrite`) ou incremental (`merge`).
"""

dbutils.widgets.dropdown("reprocessar", "False", ["True", "False"], "Reprocessar dimensão?")
reprocessar = dbutils.widgets.get("reprocessar") == "True"
```


```python
spark.sql(f"""
CREATE TABLE IF NOT EXISTS {delta_table_name} (
     sk_empresas BIGINT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
     codigo_ficticio           INT,
     doc_empresa             STRING,
     nome_razao_social            STRING,
     nome_fantasia             STRING,
     logradouro          STRING,
     inscricao_estadual       STRING,
     inscricao_municipal      STRING,
     complemento_endereco         STRING,
     codigo_postal                 STRING,
     bairro              STRING,
     codigo_cidade              INT,
     regiao                    STRING,
     responsavel_regional            STRING,
     categoria_porte                   STRING,
     data_abertura_atividade     DATE,
     data_abertura_empresa    STRING,
     dias_atividade      STRING,
     horario_atividade   STRING,
     segmento               STRING,
     tem_gnv              STRING,
     tem_etanol           STRING,
     tem_supervisor       STRING,
     qtd_funcionarios         STRING,
     tem_diesel            STRING,
     tem_troca_oleo              STRING,
     codigo_externo                     STRING,
     marca_parceira                STRING,
     email_contato                  STRING,
     email_gerente               STRING,
     tamanho_loja                 STRING,
     situacao                  STRING,
     data_encerramento         STRING,
     data_insercao             TIMESTAMP,
     data_atualizacao             TIMESTAMP
) 
USING DELTA
LOCATION '{delta_file}'
COMMENT '{comment_delta_table}';
""")


```


```python
spark.sql(f"""

select
     cod_empresa
    ,num_cnpj
    ,nom_fantasia
    ,nom_razao_social
    ,logradouro
    ,inscricao_estadual
    ,inscricao_municipal
    ,complemento_endereco
    ,codigo_postal
    ,bairro
    ,codigo_cidade
from {environment}.trusted.tb_tab_empresa_farol
where 1=1
""").createOrReplaceTempView('tab_empresa')
```


```python
spark.sql(f"""

select
     codigo
    ,regiao
    ,categoria_porte
    ,tamanho_loja
    ,regiao
    ,ga 
    ,categoria_porte 
    ,data_abertura
    ,dias_de_func 
    ,horario_de_func 
    ,segmento
    ,tem_gnv
    ,tem_etanol
    ,tem_supervisor
    ,qtd_funcionarios
    ,tem_diesel
    ,tem_troca_oleo
    ,codigo_externo
    ,marca_parceira
    ,email_contato
    ,email_gerente
    ,tamanho_loja
    ,situacao
    ,data_encerramento
from {environment}.raw.sharepoint_dados_filiais
where 1=1;

""").createOrReplaceTempView('dados_filiais')
```


```python
spark.sql(f"""

select
     cod_empresa
    ,to_date(min(data), 'yyyy-MM-dd') as data_abertura_filial
from {environment}.camada_destino.tb_farol_faturamento
where 1=1
group by
    cod_empresa;

""").createOrReplaceTempView('tab_faturamento')
```


```python
source_df = spark.sql("""
                      
select 
     emp.cod_empresa as codigo_ficticio
    ,emp.num_cnpj as doc_empresa
    ,emp.nom_razao_social as nome_razao_social
    ,emp.nom_fantasia as nome_fantasia
    ,emp.logradouro
    ,emp.inscricao_estadual
    ,emp.inscricao_municipal
    ,emp.complemento_endereco
    ,emp.codigo_postal
    ,emp.bairro
    ,emp.codigo_cidade
    ,fil.regiao
    ,fil.ga as responsavel_regional
    ,fil.categoria_porte as categoria_porte
    ,fat.data_abertura_filial as data_abertura_atividade
    ,fil.data_abertura as data_abertura_empresa
    ,fil.dias_de_func as dias_atividade
    ,fil.horario_de_func as horario_atividade
    ,fil.segmento
    ,fil.tem_gnv
    ,fil.tem_etanol
    ,fil.tem_supervisor
    ,fil.qtd_funcionarios
    ,fil.tem_diesel
    ,fil.tem_troca_oleo
    ,fil.codigo_externo
    ,fil.marca_parceira
    ,fil.email_contato
    ,fil.email_gerente
    ,fil.tamanho_loja
    ,fil.situacao
    ,fil.data_encerramento
from tab_empresa emp
left join dados_filiais fil
    on emp.cod_empresa = fil.codigo
left join tab_faturamento fat
    on emp.cod_empresa = fat.cod_empresa
where 1=1
order by emp.nom_fantasia
""")

source_df.createOrReplaceTempView('source_df')
```


```python
if reprocessar:
  source_df = source_df.withColumn("data_insercao", lit(current_timestamp() ) )
  source_df.write.format("delta")\
    .mode("overwrite")\
    .saveAsTable(f"{delta_table_name}", path=f"{delta_file}")
  print(f"Carga overwrite realizada com sucesso! {delta_table_name}")
else:
  print("Realizando carga em Merge..")
  spark.sql(f"""

MERGE INTO {delta_table_name} AS target
USING source_df AS source
  ON target.codigo_ficticio = source.codigo_ficticio
WHEN MATCHED THEN
  UPDATE SET
    target.doc_empresa            = source.doc_empresa,
    target.nome_razao_social           = source.nome_razao_social,
    target.nome_fantasia           = source.nome_fantasia,
    target.logradouro         = source.logradouro,
    target.inscricao_estadual      = source.inscricao_estadual,
    target.inscricao_municipal     = source.inscricao_municipal,
    target.complemento_endereco        = source.complemento_endereco,
    target.codigo_postal                = source.codigo_postal,
    target.bairro             = source.bairro,
    target.codigo_cidade             = source.codigo_cidade,
    target.regiao                   = source.regiao,
    target.responsavel_regional           = source.responsavel_regional,
    target.categoria_porte                  = source.categoria_porte,
    target.data_abertura_atividade    = source.data_abertura_atividade,
    target.data_abertura_empresa   = source.data_abertura_empresa,
    target.dias_atividade     = source.dias_atividade,
    target.horario_atividade  = source.horario_atividade,
    target.segmento              = source.segmento,
    target.tem_gnv             = source.tem_gnv,
    target.tem_etanol          = source.tem_etanol,
    target.tem_supervisor      = source.tem_supervisor,
    target.qtd_funcionarios        = source.qtd_funcionarios,
    target.tem_diesel           = source.tem_diesel,
    target.tem_troca_oleo             = source.tem_troca_oleo,
    target.codigo_externo                    = source.codigo_externo,
    target.marca_parceira               = source.marca_parceira,
    target.email_contato                 = source.email_contato,
    target.email_gerente              = source.email_gerente,
    target.tamanho_loja                = source.tamanho_loja,
    target.situacao                 = source.situacao,
    target.data_encerramento        = source.data_encerramento,
    target.data_atualizacao            = current_timestamp()
WHEN NOT MATCHED THEN
  INSERT (
    codigo_ficticio,
    doc_empresa,
    nome_razao_social,
    nome_fantasia,
    logradouro,
    inscricao_estadual,
    inscricao_municipal,
    complemento_endereco,
    codigo_postal,
    bairro,
    codigo_cidade,
    regiao,
    responsavel_regional,
    categoria_porte,
    data_abertura_atividade,
    data_abertura_empresa,
    dias_atividade,
    horario_atividade,
    segmento,
    tem_gnv,
    tem_etanol,
    tem_supervisor,
    qtd_funcionarios,
    tem_diesel,
    tem_troca_oleo,
    codigo_externo,
    marca_parceira,
    email_contato,
    email_gerente,
    tamanho_loja,
    situacao,
    data_encerramento,
    data_insercao
  )
  VALUES (
    source.codigo_ficticio,
    source.doc_empresa,
    source.nome_razao_social,
    source.nome_fantasia,
    source.logradouro,
    source.inscricao_estadual,
    source.inscricao_municipal,
    source.complemento_endereco,
    source.codigo_postal,
    source.bairro,
    source.codigo_cidade,
    source.regiao,
    source.responsavel_regional,
    source.categoria_porte,
    source.data_abertura_atividade,
    source.data_abertura_empresa,
    source.dias_atividade,
    source.horario_atividade,
    source.segmento,
    source.tem_gnv,
    source.tem_etanol,
    source.tem_supervisor,
    source.qtd_funcionarios,
    source.tem_diesel,
    source.tem_troca_oleo,
    source.codigo_externo,
    source.marca_parceira,
    source.email_contato,
    source.email_gerente,
    source.tamanho_loja,
    source.situacao,
    source.data_encerramento,
    current_timestamp()
    )
  
  """)
```
