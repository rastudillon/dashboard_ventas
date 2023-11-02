import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import locale
# import missingno as msn
# from PIL import Image

st.set_page_config(layout="wide", page_title="Dashboard", page_icon=":chart_with_upwards_trend:", initial_sidebar_state="expanded")

@st.cache_data
def cargar_csv(csv):
    df = pd.read_csv(csv,encoding="latin1",sep=";")
    # df = df.drop(["canal","num_reserva","estadocab","nombre","direc","tipo_rt","num_detalle","sku","estadodet","fec_desp","pais","latitude","longitude"],axis=1)
    df["total"] = df.cantidad*df.precio
    df.fec_reserva = pd.to_datetime(df.fec_reserva, format='%d-%m-%Y')
    df["mes"] = df.fec_reserva.dt.strftime("%B")
    df["año"] = df.fec_reserva.dt.strftime("%Y")
    return df

def filtros_dashboard(df):
    st.sidebar.title("Filtros")
    ciudad = st.sidebar.selectbox("Ciudad",df.ciudad.unique().tolist())
    return df[df.ciudad == ciudad]

def venta_total(df,titulo):
    total = round(df.total.sum())
    locale.setlocale(locale.LC_ALL, "")
    total_formateado = locale.format_string("%d",total,grouping=True)

    color = 'color: black; font-size: 27px; text-align: center'
    div_style = "background: linear-gradient(to right, #0075A2, #00FFC5);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:black;margin-bottom:10px;"
    titulo = titulo

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>${total_formateado}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def max_venta(df):
    pd.options.display.float_format= "{:.0f}".format
    ventas_diarias = pd.DataFrame(df.total.groupby(df.fec_reserva.dt.date).sum())
    dia_mayor_venta = round(ventas_diarias.total.max())
    dia = ventas_diarias.idxmax().values[0]
    locale.setlocale(locale.LC_ALL, "")
    max_formateado = locale.format_string("%d",dia_mayor_venta,grouping=True)

    color = 'color: black; font-size: 27px; text-align: center'
    div_style = "background: linear-gradient(to right, #0075A2, #00FFC5);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:black;margin-bottom:10px;"
    titulo = "Fecha top de ventas ({})".format(dia)

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>${max_formateado}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def articulo_recaudaciones_top(df):
    articulos = pd.DataFrame(df.total.groupby(df.sku_nom).sum())
    top_monto = round(articulos.max())
    top_id = articulos.idxmax().values[0]
    locale.setlocale(locale.LC_ALL, "")
    max_formateado = locale.format_string("%d",top_monto,grouping=True)

    color = 'color: black; font-size: 27px; text-align: center'
    div_style = "background: linear-gradient(to right, #0075A2, #00FFC5);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:black;margin-bottom:10px;"
    titulo = "El artículo {} genero mas ganancias".format(top_id)

    metric_html = f"<div style= '{div_style}'>"\
        f"<span style= '{title_style}'>{titulo}</span></br>"\
        f"<span style= '{color}'>${max_formateado}</span></div>"
    
    return st.write(metric_html,unsafe_allow_html=True)

def ventas_por_ciudad(df):
    agrupacion_ventas_ciudad = (df.groupby("ciudad")["total"].sum()/31).reset_index()
    fig = px.bar(agrupacion_ventas_ciudad, x="ciudad",y="total",color="ciudad")

    fig.update_layout(xaxis_title='Ciudad',
                      yaxis_title='Total de ventas',
                      title={
                          "text":"Venta mensual total por ciudad",
                          "x":0.5,
                          "xanchor": "center"},
                      title_font_color= "#D8E2DC", height=255)
    
    st.plotly_chart(fig,use_container_width=True)

def evolucion_diaria_ventas(df):
    ventas_diarias = df.groupby(df.fec_reserva.dt.date)["total"].sum().reset_index()
    fig = px.area(ventas_diarias, x="fec_reserva",y="total")

    fig.update_layout(xaxis_title='Fecha',
                      yaxis_title='Total',
                      title={
                          "text":"Venta mensual total por ciudad",
                          "x":0.5,
                          "xanchor": "center"},
                      title_font_color= "#D8E2DC", height=255)
    
    st.plotly_chart(fig,use_container_width=True)

def top_articulos(df):
    ventas_por_articulos = df.groupby("sku_nom")["total"].sum().reset_index()
    ventas_articulos_filtrado = ventas_por_articulos[ventas_por_articulos.total>=462182972] 
    fig = px.pie(ventas_articulos_filtrado,values="total",names="sku_nom",hole=.5)

    fig.update_layout(
        title={
            "text":"Top 10 articulos que generaron mas ganancias",
            "x":0.5,
            "xanchor": "center"},
        title_font_color= "#D8E2DC",
        font={
            "size":13}, height=350)

    st.plotly_chart(fig,use_container_width=True)  

def dashboard(df):
    filtro = filtros_dashboard(df)

    m1,m2,m3 = st.columns(3)
    with m1:
        ventas_por_ciudad(df)
    with m2:
        evolucion_diaria_ventas(df)
    with m3:
        top_articulos(df)

    m1,m2,m3 = st.columns(3)
    with m1:
        venta_total(df,"Total ventas Enero")
    with m2:
        max_venta(df)
    with m3:
        articulo_recaudaciones_top(df)
    m1,m2,m3 = st.columns(3)
    with m1:
        venta_total(filtro,"Total ventas ciudad")
    with m2:
        max_venta(filtro)
    with m3:
        articulo_recaudaciones_top(filtro)

def main():
    st.title("Dashboard para el análisis de ventas")
    csv = st.sidebar.file_uploader("Elija archivo CSV",type=["csv"])
    if csv is not None:
        df = cargar_csv(csv)
        dashboard(df)

main()
