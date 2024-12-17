import streamlit as st
from clickhouse_driver import Client
import time
import pandas as pd
import plotly.express as px


client = Client(host='localhost', port=9000)

list_market = ['OZON', 'Wildberries','Яндекс Маркет', 're:Store','Мегамаркет','М.Видео',
              'Эльдорадо', 'Ситилинк','DNS', 'Технопарк','Связной','Билайн','Мегафон','t2']

list_prod = ['iPhone 16','iPhone 16 Plus','iPhone 16 Pro','iPhone 16 Pro Max', 
            'Apple Watch 10','Apple Watch Ultra 2','AirPods 4','AirPods Max', 
            'iPad','iPad Pro','iPad Air','iPad mini', 'Vision Pro','MacBook Air', 'MacBook Pro']

def get_sum():
    result = client.execute('SELECT sum(value) as total FROM kafka_messages_local')
    return result[0][0] if result[0][0] is not None else 0

def get_recent_rows(select_prods, selected_markets, k=50, val_min=5):
    result = client.execute(f'''
        SELECT *
        FROM kafka_messages_local
        where time > now() - interval '{val_min} minutes'
            and market in (
                    {"'" + "', '".join(selected_markets) + "'"}
                )
            and product in (
                {"'" + "', '".join(select_prods) + "'"}
            )
        ORDER BY time DESC
        LIMIT {k}
    ''')
    return pd.DataFrame(result, columns=['market', 'country', 'product', 'color', 'price', 'time', 'processed_dttm'])

def get_top_popular_products(k=5, val_min=5):
    result = client.execute(f'''
        SELECT 
            product
            , count(*) as cnt
        FROM kafka_messages_local
        where time >= now() - interval '{val_min} minutes'
        group by 1
        ORDER BY 2 desc
        LIMIT {k}
    ''')
    return pd.DataFrame(result, columns=['product', 'cnt'])

def get_top_popular_market(k=5, val_min=5):
    result = client.execute(f'''
        SELECT 
            market
            , count(*) as cnt
        FROM kafka_messages_local
        where time >= now() - interval '{val_min} minutes'
        group by 1
        ORDER BY 2 desc
        LIMIT {k}
    ''')
    return pd.DataFrame(result, columns=['market', 'cnt'])

def get_avg_price(val_min=5):
    result = client.execute(f'''
        SELECT 
            product
            , avg(price) as avg_price
        FROM kafka_messages_local
        where time >= now() - interval '{val_min} minutes'
        group by 1
        ORDER BY 1
    ''')
    return pd.DataFrame(result, columns=['market', 'cnt'])

def main():

    st.title("MARAD (Market Radar)")

    multi_select_market=st.multiselect("Маркетплейсы:", options=list_market, default=list_market)

    multi_select_prod=st.multiselect("Товары:", options=list_prod, default=list_prod)

    val_min=st.slider("Показывать за последние (минут):", min_value=1, max_value=150, value=10)

    st.subheader("Последние объявления:")
    df1 = get_recent_rows(select_prods=multi_select_prod, selected_markets=multi_select_market, val_min=val_min)
    st.dataframe(df1)

    st.subheader("Топ популярных продуктов:")
    fig_product_col1, fig_product_col2 = st.columns(2)
    df2 = get_top_popular_products(val_min=val_min)
    with fig_product_col1:
        st.dataframe(df2)
    
    with fig_product_col2:
        fig2 = px.pie(df2, values='cnt', names='product')
        st.write(fig2)

    st.subheader("Топ площадок по количеству объявлений:")
    df3 = get_top_popular_market(val_min=val_min)
    st.dataframe(df3)

    fig = px.pie(df3, values='cnt', names='market')

    st.subheader("Текущая средняя цена на товары:")
    df4 = get_avg_price(val_min=val_min)
    st.dataframe(df4)

if __name__ == '__main__':
    main()