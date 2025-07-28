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

container_target = 'refined'
directory = 'farol'
table_name = 'd_empresas_farol'
delta_table_name = f'{environment}.{container_target}.{table_name}'
delta_file = f"abfss://{container_target}@{data_lake_name}.dfs.core.windows.net/{directory}/{table_name}/"
comment_delta_table = 'Tabela de dimensão de Empresas...'

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
     codigo_empresa           INT,
     cnpj_empresa             STRING,
     razao_social            STRING,
     nome_empresa             STRING,
     des_logradouro          STRING,
     num_insc_estadual       STRING,
     num_insc_municipal      STRING,
     des_complemento         STRING,
     num_cep                 STRING,
     nom_bairro              STRING,
     cod_cidade              INT,
     area                    STRING,
     gerente_area            STRING,
     porte                   STRING,
     data_abertura_cupom     DATE,
     data_abertura_empresa    STRING,
     dias_funcionamento      STRING,
     horario_funcionamento   STRING,
     categoria               STRING,
     possui_gnv              STRING,
     possui_etanol           STRING,
     possui_supervisor       STRING,
     quadro_aprovado         STRING,
     pista_diesel            STRING,
     troca_oleo              STRING,
     sss                     STRING,
     bandeira                STRING,
     e_mail                  STRING,
     e_mail_ga               STRING,
     m2_loja                 STRING,
     status                  STRING,
     data_inativacao         STRING,
     insert_date             TIMESTAMP,
     update_date             TIMESTAMP
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
    ,des_logradouro
    ,num_insc_estadual
    ,num_insc_municipal
    ,des_complemento
    ,num_cep
    ,nom_bairro
    ,cod_cidade
from {environment}.trusted.tb_tab_empresa_farol
where 1=1
""").createOrReplaceTempView('tab_empresa')
```


```python
spark.sql(f"""

select
     codigo
    ,area
    ,porte
    ,m2_loja
    ,area
    ,ga 
    ,porte 
    ,data_abertura
    ,dias_de_func 
    ,horario_de_func 
    ,categoria
    ,possui_gnv
    ,possui_etanol
    ,possui_supervisor
    ,quadro_aprovado
    ,pista_diesel
    ,troca_oleo
    ,sss
    ,bandeira
    ,e_mail
    ,e_mail_ga
    ,m2_loja
    ,status
    ,data_inativacao
from {environment}.raw.sharepoint_dados_filiais
where 1=1;

""").createOrReplaceTempView('dados_filiais')
```


```python
spark.sql(f"""

select
     cod_empresa
    ,to_date(min(data), 'yyyy-MM-dd') as data_abertura_filial
from {environment}.refined.tb_farol_faturamento
where 1=1
group by
    cod_empresa;

""").createOrReplaceTempView('tab_faturamento')
```


```python
source_df = spark.sql("""
                      
select 
     emp.cod_empresa as codigo_empresa
    ,emp.num_cnpj as cnpj_empresa
    ,emp.nom_razao_social as razao_social
    ,emp.nom_fantasia as nome_empresa
    ,emp.des_logradouro
    ,emp.num_insc_estadual
    ,emp.num_insc_municipal
    ,emp.des_complemento
    ,emp.num_cep
    ,emp.nom_bairro
    ,emp.cod_cidade
    ,fil.area
    ,fil.ga as gerente_area
    ,fil.porte as porte
    ,fat.data_abertura_filial as data_abertura_cupom
    ,fil.data_abertura as data_abertura_empresa
    ,fil.dias_de_func as dias_funcionamento
    ,fil.horario_de_func as horario_funcionamento
    ,fil.categoria
    ,fil.possui_gnv
    ,fil.possui_etanol
    ,fil.possui_supervisor
    ,fil.quadro_aprovado
    ,fil.pista_diesel
    ,fil.troca_oleo
    ,fil.sss
    ,fil.bandeira
    ,fil.e_mail
    ,fil.e_mail_ga
    ,fil.m2_loja
    ,fil.status
    ,fil.data_inativacao
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
  source_df = source_df.withColumn("insert_date", lit(current_timestamp() ) )
  source_df.write.format("delta")\
    .mode("overwrite")\
    .saveAsTable(f"{delta_table_name}", path=f"{delta_file}")
  print(f"Carga overwrite realizada com sucesso! {delta_table_name}")
else:
  print("Realizando carga em Merge..")
  spark.sql(f"""

MERGE INTO {delta_table_name} AS target
USING source_df AS source
  ON target.codigo_empresa = source.codigo_empresa
WHEN MATCHED THEN
  UPDATE SET
    target.cnpj_empresa            = source.cnpj_empresa,
    target.razao_social           = source.razao_social,
    target.nome_empresa           = source.nome_empresa,
    target.des_logradouro         = source.des_logradouro,
    target.num_insc_estadual      = source.num_insc_estadual,
    target.num_insc_municipal     = source.num_insc_municipal,
    target.des_complemento        = source.des_complemento,
    target.num_cep                = source.num_cep,
    target.nom_bairro             = source.nom_bairro,
    target.cod_cidade             = source.cod_cidade,
    target.area                   = source.area,
    target.gerente_area           = source.gerente_area,
    target.porte                  = source.porte,
    target.data_abertura_cupom    = source.data_abertura_cupom,
    target.data_abertura_empresa   = source.data_abertura_empresa,
    target.dias_funcionamento     = source.dias_funcionamento,
    target.horario_funcionamento  = source.horario_funcionamento,
    target.categoria              = source.categoria,
    target.possui_gnv             = source.possui_gnv,
    target.possui_etanol          = source.possui_etanol,
    target.possui_supervisor      = source.possui_supervisor,
    target.quadro_aprovado        = source.quadro_aprovado,
    target.pista_diesel           = source.pista_diesel,
    target.troca_oleo             = source.troca_oleo,
    target.sss                    = source.sss,
    target.bandeira               = source.bandeira,
    target.e_mail                 = source.e_mail,
    target.e_mail_ga              = source.e_mail_ga,
    target.m2_loja                = source.m2_loja,
    target.status                 = source.status,
    target.data_inativacao        = source.data_inativacao,
    target.update_date            = current_timestamp()
WHEN NOT MATCHED THEN
  INSERT (
    codigo_empresa,
    cnpj_empresa,
    razao_social,
    nome_empresa,
    des_logradouro,
    num_insc_estadual,
    num_insc_municipal,
    des_complemento,
    num_cep,
    nom_bairro,
    cod_cidade,
    area,
    gerente_area,
    porte,
    data_abertura_cupom,
    data_abertura_empresa,
    dias_funcionamento,
    horario_funcionamento,
    categoria,
    possui_gnv,
    possui_etanol,
    possui_supervisor,
    quadro_aprovado,
    pista_diesel,
    troca_oleo,
    sss,
    bandeira,
    e_mail,
    e_mail_ga,
    m2_loja,
    status,
    data_inativacao,
    insert_date
  )
  VALUES (
    source.codigo_empresa,
    source.cnpj_empresa,
    source.razao_social,
    source.nome_empresa,
    source.des_logradouro,
    source.num_insc_estadual,
    source.num_insc_municipal,
    source.des_complemento,
    source.num_cep,
    source.nom_bairro,
    source.cod_cidade,
    source.area,
    source.gerente_area,
    source.porte,
    source.data_abertura_cupom,
    source.data_abertura_empresa,
    source.dias_funcionamento,
    source.horario_funcionamento,
    source.categoria,
    source.possui_gnv,
    source.possui_etanol,
    source.possui_supervisor,
    source.quadro_aprovado,
    source.pista_diesel,
    source.troca_oleo,
    source.sss,
    source.bandeira,
    source.e_mail,
    source.e_mail_ga,
    source.m2_loja,
    source.status,
    source.data_inativacao,
    current_timestamp()
    )
  
  """)
```
