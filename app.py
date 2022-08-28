import streamlit as st
import pandas as pd

import pickle
import requests

ops = pickle.load(open('cos2_vector.pkl','rb'))
simi = pickle.load(open('eu_vector.pkl','rb'))

freq = pickle.load(open('freq_t.pkl','rb'))
freq_t = pd.DataFrame(freq)

we1 = pickle.load(open('we1.pkl','rb'))
we = pd.DataFrame(we1)

main3 = pickle.load(open('main3.pkl','rb'))
main = pd.DataFrame(main3)

s3 = pickle.load(open('s7.pkl','rb'))
s = pd.DataFrame(s3)

s['StockCode'] = s['StockCode'].astype(str)

main['StockCode'] = main['StockCode'].astype(str)


def similiar_cust_prod(id):
    index = we[we['CustomerID'] == int(id)].index[0]
    similarity_vec = simi[index]
    m = sorted(list(enumerate(similarity_vec)), key=lambda x: x[1])[1:6]
    f = []
    for i in m:
        cid = we['CustomerID'].iloc[i[0]]
        f.append(freq_t[freq_t['CustomerID'] == cid].iloc[0]['Description'])
    return f

def cbf(pid):
    index = s[s['StockCode'] == pid].index[0]
    similarity_vec = ops[index]
    m = sorted(list(enumerate(similarity_vec)) ,  reverse = True ,   key = lambda x:x[1])[1:6]
    r = []
    for i in m:
        k = s['StockCode'].iloc[i[0]]
        r.append(main[main['StockCode'] == k]['Description'].iloc[0])

    return r



st.title('E-commerce - Recommender System')


selected_cust_id = st.selectbox(
        'select your cust id' ,
        we['CustomerID'].values)

selected_product = st.selectbox(
    'select the product',
    freq_t['Description'].values)

if st.button("recommend"):
    st.header("recommended products based on your selection")
    sid = main[main['Description'] == selected_product]['StockCode'].iloc[0]
    h = cbf(str(sid))
    for i in h:
        st.write(i)

    st.header("customers with similiar interest also buys")
    p = similiar_cust_prod(selected_cust_id)
    for i in p:
        st.write(i)





