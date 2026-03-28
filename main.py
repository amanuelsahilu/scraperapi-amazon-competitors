import streamlit as st
import time
from src.scraper_api import scrape_product_detail,render_product_detail,scrape_competitor_product
# from src.services import scrape_and_store_products


def render_header():
    st.title("Amazon Competitor Analysis")
    st.caption("Enter your ASIN to get product insights.")

def render_input():
    asin = st.text_input("ASIN",placeholder = 'eg.xxxxxxxxxxxx')
    product_name = st.text_input("Product Name",placeholder = 'eg.xxxxxxxxxxxx')
    geo = st.text_input("Zip/Postal Code",placeholder = 'eg.xxxxxxxx')
    domain = st.selectbox("Domain", {
        'com','ca','co.uk'
    })

    return asin.strip(),geo.strip(),domain

def main():
    st.set_page_config(
    page_title = 'AMAZON competitor Analysis',
    page_icon = '🆒',
        layout = 'wide'
    )
    render_header()
    asin,geo,domain = render_input()

    if asin and st.button('Scrap Product'):
        st.session_state.rerun = True
        with st.spinner("Scrapping Product ..."):
            product_detail = scrape_product_detail(asin,domain)
            scrape_competitor_product(product_detail)
        render_product_detail(product_detail)



if __name__ == '__main__':
    main()


