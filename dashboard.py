import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import locale
# import missingno as msn
# from PIL import Image

st.set_page_config(layout="wide", page_title="Dashboard", page_icon=":chart_with_upwards_trend:", initial_sidebar_state="collapsed")

@st.cache_data
def cargar_csv(csv):
    df = pd.read_csv(csv,encoding="latin1",sep=";")
    # df = df.drop(["canal","num_reserva","estadocab","nombre","direc","tipo_rt","num_detalle","sku","estadodet","fec_desp","pais","latitude","longitude"],axis=1)
    df["total"] = df.cantidad*df.precio
    df.fec_reserva = pd.to_datetime(df.fec_reserva, format='%d-%m-%Y')
    df["mes"] = df.fec_reserva.dt.strftime("%B")
    df["año"] = df.fec_reserva.dt.strftime("%Y")
    return df

def venta_total_anual(df):
    total = round(df.total.sum())
    locale.setlocale(locale.LC_ALL, "")
    total_formateado = locale.format_string("%d",total,grouping=True)

    color = 'color: black; font-size: 27px; text-align: center'
    div_style = "background: linear-gradient(to right, #0075A2, #00FFC5);padding:1px;border-radius:5px;text-align:center;"
    title_style = "font-size:13px;font-weight:lighter;color:black;margin-bottom:10px;"
    titulo = "Total ventas"

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

def dashboard(df):
    m1,m2,m3 = st.columns(3)
    with m1:
        venta_total_anual(df)
    m1,m2,m3 = st.columns(3)
    with m1:
        max_venta(df)
    m1,m2,m3 = st.columns(3)
    with m1:
        articulo_recaudaciones_top(df)

def main():
    st.title("Dashboard para el análisis de ventas")
    csv = st.sidebar.file_uploader("Elija archivo CSV",type=["csv"])
    if csv is not None:
        df = cargar_csv(csv)
        dashboard(df)

main()