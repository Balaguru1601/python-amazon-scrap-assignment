from bs4 import BeautifulSoup
import requests
import csv

for i in range(9, 19):
    try:
        print(i)
        product_data = {}
        URL = f"https://www.amazon.in/s?k=bags&page={i + 1}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
                  "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8"}

        response = requests.get(URL, headers=header)
        content = response.text

        soup = BeautifulSoup(content, "html.parser")
        all_box = soup.find_all(name="div",
                                class_="s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis "
                                       "s-latency-cf-section s-card-border")

        for box in all_box:
            title = box.find(name="span", class_="a-size-medium a-color-base a-text-normal").get_text()
            stars = box.find(name="span", class_="a-icon-alt").get_text()
            product_link = \
                box.find(name="a",
                         class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"]
            product_link = "https://www.amazon.in" + product_link
            price = box.find(name="span", class_="a-price-whole").get_text()
            product_page = requests.get(product_link, headers=header)
            product_content = product_page.text

            product_soup = BeautifulSoup(product_content, "html.parser")
            no_of_ratings = 0
            try:
                no_of_ratings = product_soup.find(name="span", id="acrCustomerReviewText").get_text().split(" ")[0]
            except AttributeError:
                no_of_ratings = 0
            description = ""
            try:
                description_ul = product_soup.find(name="div", id="feature-bullets").find_all(name="li")
                for desc in description_ul:
                    description += desc.get_text() + "\\"
            except AttributeError:
                continue
            product_description = ""
            asin = ""
            manufacturer = ""
            try:
                details_div = product_soup.find(name="div", id="detailBulletsWrapper_feature_div")
                details_items = details_div.find_all(name="span", class_="a-text-bold")
                for detail in details_items:
                    if detail.get_text().find("ASIN") != -1:
                        asin = detail.find_next_sibling(name="span").get_text()
                    elif detail.get_text().find("Manufacturer") != -1:
                        manufacturer = detail.find_next_sibling(name="span").get_text()
            except AttributeError:
                details_div = product_soup.find(name="table", id="productDetails_detailBullets_sections1")
                details_items = details_div.find_all(name="th")
                for detail in details_items:
                    if detail.get_text().find("ASIN") != -1:
                        asin = detail.find_next(name="td").get_text()
                tech_details = product_soup.find(name="table", id="productDetails_techSpec_section_1")
                tech_detail_items = tech_details.find_all("th")
                for detail in tech_detail_items:
                    if detail.get_text().find("Manufacturer") != -1:
                        manufacturer = detail.find_next(name="td").get_text().strip()
                        break

            try:
                product_description = product_soup.find(name="div", id="productDescription").find(name="span").get_text()
            except AttributeError:
                product_description = "Not available"

            product_data["title"] = title
            product_data["product_link"] = product_link
            product_data["product_price"] = price
            product_data["product_rating"] = stars
            product_data["no_of_ratings"] = no_of_ratings
            product_data["description"] = description
            product_data["asin"] = asin
            product_data["manufacturer"] = manufacturer
            product_data["product_description"] = product_description
            print(product_data)
            with open("data.csv", "a", encoding="utf-8") as file:
                fields = ["title", "product_link", "product_price", "product_rating", "no_of_ratings", "description", "asin",
                          "manufacturer", "product_description"]
                writer = csv.DictWriter(file, fields)
                writer.writerow(product_data)

    except AttributeError:
        print("error")
        continue
