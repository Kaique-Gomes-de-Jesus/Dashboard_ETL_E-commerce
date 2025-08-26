# Importando bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

#Títudo do dash
st.title("Dashboard E-commerce")
st.markdown("Visualização interativa das métricas e gráficos do e-commerce")

#Carregando base de dados
df_final= pd.read_csv("planilha_final_analise_ecommerce.csv")


#Métricas principais
qtd_clientes_unicos = df_final['id_cliente_unico'].nunique()
numero_pedidos_cliente = df_final.groupby('id_cliente_unico')['id_pedido'].nunique()
qtd_tipo_pagamento = df_final['tipo_pagamento'].value_counts()
qtd_pedidos = df_final['id_pedido'].count()

#Exibindo as métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Clientes Únicos", qtd_clientes_unicos, border=True)
col2.metric("Tipo de Pagamento mais usado", str(qtd_tipo_pagamento.index[0]), border=True)
col3.metric("Quantidade Total de Pedidos", qtd_pedidos, border=True)

#Título sidebar
st.sidebar.header('Filtros')
# Filtro de estados
estados_disponiveis = df_final['estado_cliente'].unique()
estados_selecionados = st.sidebar.multiselect(
    "Selecione os estados para comparar:",
    options=sorted(estados_disponiveis),
    default=list(sorted(estados_disponiveis))[:3] #Seleciona os 3 primeiros por padrão
)

#Verificando se tem estados selecionados
if len(estados_selecionados) == 0:
    st.warning('Nenhum estado selecionado para comparar!')
else:
    # Filtrando o DataFrame
    df_filtrado = df_final[df_final['estado_cliente'].isin(estados_selecionados)]

    #Gráfico de Clientes por Estado
    qtd_clientes_estado = df_filtrado.groupby('estado_cliente')['id_cliente_unico'].nunique().sort_values(ascending=False)
    fig1 = px.bar(qtd_clientes_estado, x=qtd_clientes_estado.values[::-1], y=qtd_clientes_estado.index[::-1],
                labels={'y': 'Estados', 'x':'Clientes', 'color':'Estados'},
                title="Quantidade de Clientes por Estado ",
                orientation='h',
                color=qtd_clientes_estado.index[::-1]
                )
    #Configurando gráfico
    fig1.update_layout(
                    font_family = 'Arial',
                    font_size = 20,
                    title_font_size = 26,
                    )

    st.plotly_chart(fig1)


# Filtro de categorias
categorias_disponíveis = df_final['categoria_produto'].dropna().unique()
categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as categorias para comparar:",
    options=categorias_disponíveis,
    default=list((categorias_disponíveis))[:3] #Seleciona os 3 primeiros por padrão
)

#Verificando se tem categorias selecionadas
if len(categorias_selecionadas) == 0:
    st.warning('Nenhuma categoria selecionada para comparar!')
else:
    # Filtrando o DataFrame
    df_filtrado_categorias = df_final[df_final['categoria_produto'].isin(categorias_selecionadas)]

    # Gráfico das Categorias Mais Vendidas
    produtos_vendidos_categoria = df_filtrado_categorias['categoria_produto'].value_counts()
    fig2 = px.bar(produtos_vendidos_categoria, x=produtos_vendidos_categoria.values[::-1], y=produtos_vendidos_categoria.index[::-1],
                labels={'y':'Categorias', 'x':'Quantidade vendida', 'color':'Categorias'},
                title="Quantidade de vendas por categorias ",
                orientation='h',
                color=produtos_vendidos_categoria.index[::-1]
                )
    fig2.update_layout(
                    font_family = 'Arial',
                    font_size = 20,
                    title_font_size = 26,
                    showlegend = False
                    )
    st.plotly_chart(fig2)

#Gráfico de Proporção dos Métodos de Pagamento
qtd_tipo_pagamento = df_final['tipo_pagamento'].value_counts()
fig3 = px.pie(values=qtd_tipo_pagamento.values, names=qtd_tipo_pagamento.index, 
              title="Proporção dos Métodos de Pagamento",
              )
fig3.update_layout(
                  font_family = 'Arial',
                  font_size = 20,
                  title_font_size = 26
                  )
st.plotly_chart(fig3)

#Gráfico do Top 5 Vendedores com Maior Receita
receita_total_vendedor = df_final.groupby('id_vendedor')['valor_pagamento'].sum().sort_values(ascending=False).head(5)
fig4 = px.bar(receita_total_vendedor, x=receita_total_vendedor.index, y=receita_total_vendedor.values,
              labels={'y':'Receita Total', 'x':'Vendedor'},
              title="Top 5 Vendedores com Maior Receita",
              color=receita_total_vendedor.index
              )
fig4.update_layout(
                  font_family = 'Arial',
                  font_size = 20,
                  title_font_size = 26,
                  showlegend=False
                  )
st.plotly_chart(fig4)

