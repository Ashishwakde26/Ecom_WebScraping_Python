from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

URL = "https://www.amazon.in/s?k=playstation+5"

HEADERS = ({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Accept-Language': 'en-us, en;q=0.5'})

webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")

all_datas = soup.find_all("div", attrs={
    'class': 'puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v2hrdt6w0jdtp122jn0441sgwu4 s-latency-cf-section puis-card-border'})

d = {"prod_link": [], "title": [], "price": [], "rating": []}

for all_data in all_datas:
    link = all_data.find("a", attrs={
        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    prod_link = "https://amazon.in" + link.get('href')
    # print(prod_link)

    title = link.find("span", attrs={'class': 'a-size-medium a-color-base a-text-normal'}).text
    # print(title)

    try:
        rating = all_data.find("div", attrs={'class': 'a-section a-spacing-none a-spacing-top-micro'}).find("span",
                                                                                                            attrs={
                                                                                                                'class': 'a-icon-alt'}).text
    except AttributeError:
        rating = "Not Found"
    # print(rating)

    price = all_data.find("span", attrs={'class': 'a-price'}).find("span", attrs={'class': 'a-offscreen'}).text
    # print(price)

    image = all_data.find("img", attrs={"class": "s-image"}).get('src')
    # print(image)

    d['prod_link'].append(prod_link)
    d['title'].append(title)
    d['price'].append(price)
    d['rating'].append(rating)
    # print("---------------------------------------------------------------------------------------------------------------------")

# print(d)

amazon_df = pd.DataFrame.from_dict(d)
amazon_df['title'].replace('', np.nan, inplace=True)
amazon_df = amazon_df.dropna(subset=['title'])
amazon_df.to_csv("amazon_data.csv", header=True, index=False)