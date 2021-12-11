from requests_html import HTMLSession
import csv
import time

session = HTMLSession()
url = 'https://barefootbuttons.com/product-category/version-1/'


def get_links(url):
    response = session.get(url)
    items = response.html.find('div.product-small.box')
    links = []
    for item in items:
        links.append(item.find('a', first=True).attrs['href'])
    return links


def get_productdata(link):
    response = session.get(link)
    title = response.html.find('h1', first=True).full_text
    price = response.html.find(
        'span.woocommerce-Price-amount.amount bdi')[1].full_text
    tag = response.html.find('a[rel=tag]', first=True).full_text
    sku = response.html.find('span.sku', first=True).full_text

    product = {
        'title': title.strip(),
        'price': price.strip(),
        'tag': tag.strip(),
        'sku': sku.strip()
    }
    # print(product)
    return product


results = []
links = get_links(url)
# print(links)

for link in links:
    results.append(get_productdata(link))
    time.sleep(1)

print(results)

with open('products.csv', 'w', encoding='utf8', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=results[0].keys(),)
    wr.writeheader()
    wr.writerows(results)

print('successfull')
