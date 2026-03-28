import requests
from dotenv import load_dotenv
import os
import streamlit as st
from .sentence_transform import find_similarity


scraper_product_url = 'https://api.scraperapi.com/structured/amazon/product/v1'
scraper_competitor_url = 'https://api.scraperapi.com/structured/amazon/search/v1'
load_dotenv()
API_KEY = os.getenv("SCRAPER_API_KEY")

def post_query(url,payload):
    response = requests.get(url,params = payload)
    response_json = response.json()
    return response_json

def normalize_response(content):    # insert error handling
    return { 'name':content.get('name',''),
             # 'asin':content.get('product_information').get('asin','') or '',
            'full_description':content.get('full_description',''),
            'images':(content.get('images','') or ' ')[0],
            'high_res_images':(content.get('high_res_images','') or ' ')[0],
            'reviews':(content.get('reviews','') or ' ')[0],
             'price':content.get('pricing',''),
            'category':content.get('product_category',' '),
             'url':content.get('brand_url','')
             }

def scrape_product_detail(asin,domain):
    payload = {'api_key':API_KEY, 'asin': asin, 'tld':domain,'render': 'true'}
    product_json = post_query(scraper_product_url,payload)
    final_response = normalize_response(product_json)

    return final_response


def render_product_detail(product):
    with st.container(border = True,width = 'stretch'):
        cols = st.columns([1,2])

        images = product.get('high_res_images','')
        cols[0].image(images,width = 200)
        with cols[1]:
            st.subheader(f"✅{product.get('name','')}"),
            st.write(f"ASIN: {product.get('asin','')}")
            st.metric(label = 'price',value =product.get('price',''))

            if st.button('Start analyzing competitors',key = f"analyze_{product.get('asin','')}"):
                st.session_state.rerun = False
def clean_product_name(product_title):
    if '›' in product_title:
        title = product_title.split('›')
        search_title = title[-3:] #keeping the most specific categories
        final_search = " ".join([p.strip() for p in search_title])
        print(f"search keyword:{final_search}")
        return final_search
    else:
        return product_title # add additional stripping mechanism

def get_competitors(query):
    payload = {'api_key':API_KEY,'query':query,'render':'true'}
    competitor_data = post_query(scraper_competitor_url,payload)
    st.write(f"Found {len(competitor_data['results'])} competitors!")
    return competitor_data

def normalize_competitor_data(data):
    competitors = []
    ordering_criterion = []
    selected_keys = ['asin','name','image','stars','price_string']
    for item in data['results']:
        competitors.append({
            'asin':item.get('asin',''),
            'name':item.get('name',''),
            'image':item.get('image',''),
            'stars':item.get('stars',''),
            'price_string':item.get('price_string',''),
            'category': item.get('product_category', ''),
            'url':item.get('url','')
        }
        )
    return competitors


def render_competitor_detail(competitor):
    with st.container(border = True,width = 'stretch'):
        cols = st.columns([1,2])

        images = competitor.get('image','')
        cols[0].image(images,width = 200)
        with cols[1]:
            st.subheader(competitor.get('name',''))
            st.write(f"{competitor.get('stars','')}⭐ rating")
            st.metric(label = 'price',value =competitor.get('price_string',''))

            if st.button('Start analyzing competitors',key = f"analyze_{competitor.get('asin','')}"):
                st.session_state.rerun = False


def scrape_competitor_product(product):
    search_query = clean_product_name(product.get('category'))
    competitor_data = get_competitors(search_query)
    normalized_competitor_data = normalize_competitor_data(competitor_data)
    top5_indices = find_similarity(product_name = product.get('name',''),competitor_data = normalized_competitor_data)
    top5_competitors = [normalized_competitor_data[i] for i in top5_indices]
    for competitor in top5_competitors:
        render_competitor_detail(competitor)