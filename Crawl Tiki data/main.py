import requests
import pandas as pd

root_path = ""
product_id_url = "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=f39093f9-6006-7856-ddfc-18fc8c99391f&category=8095&page={}&src=c.8095.hamburger_menu_fly_out_banner&_lc=&urlKey=laptop"
product_detail_url = "https://tiki.vn/api/v2/products/{}"

def crawl_product_id():
    list_product_id = []
    page_num = 1

    while (True):
        payload={}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.request("GET", product_id_url.format(page_num), headers=headers, data=payload)

        if response.status_code == 200:
            resp = response.json()
            # exit if having no data
            if not resp["data"]:
                break
            
            for item in resp["data"]:
                list_product_id.append(item["id"])

            page_num += 1

    print(f"Crawled {len(list_product_id)} product ids")
    return list_product_id

def crawl_product_info(list_product_id=[]):
    list_product = []
    i = 0
    for id in list_product_id:
        payload={}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.request("GET", product_detail_url.format(id), headers=headers, data=payload)

        if response.status_code == 200:
            list_product.append(response.json())

    print(f"Crawled {len(list_product)} products")
    return list_product


if __name__ == "__main__":
    list_product_id = []
    list_product = []

    # Get product_id
    list_product_id = crawl_product_id()
    # Save product_id to file
    with open(file=root_path+"product_id.txt", mode="w", encoding="utf-8") as file:
        for i in list_product_id:
            file.write(str(i) + "\n")

    # Get product detail
    if list_product_id:
        list_product = crawl_product_info(list_product_id)

        df = pd.DataFrame(list_product)
        df.to_csv(root_path+"product_detail.csv", index=False, encoding="utf-8-sig")