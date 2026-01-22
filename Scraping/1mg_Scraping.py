import json
import time
import warnings

from helper import get_faq, get_feedback, get_patient_concerns, get_side_effects
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver = webdriver.Chrome(executable_path = ".\chromedriver.exe")

site = "https://www.1mg.com"

drugs = [
    # "paracetamol",
    # "brufen",
    # "rantac",
    # "pantoprazole",
    "amoxicillin",
    "amoxiclav",
    "metronidazole",
    "ciprofloxacin",
    "ceftriaxone",
    "levocetirizine",
    "azithromycin",
    "levofloxacin"
]

drugs_data = {}

for drug in drugs:

    url = site + "/search/all?name=" + drug

    drug_data = []

    driver.get(url)
    time.sleep(5)

    page_cnt = 0
    max_page_cnt = 1

    prods_cnt = 0
    max_prods_cnt = 30

    products_urls = []

    while (page_cnt < max_page_cnt) and (prods_cnt < max_prods_cnt):

        prods = driver.find_elements("xpath","//div[contains(@class,'style__horizontal-card___1Zwmt style__height')]/a")

        prods_cnt = len(prods)

        for prod in prods:
            link = prod.get_attribute("href")

            products_urls.append(link)


        try:
            nxt_btn = driver.find_element("xpath","//span[@class='style__next___2Cubq']")
            nxt_btn.click()

            time.sleep(2)

            page_cnt += 1

        except:
            break

    # print(len(products_urls))
    print(f"\n\nFound {prods_cnt} products for {drug}")

    for i,product_link in enumerate(tqdm(products_urls)):

        driver.get(product_link)

        time.sleep(5)

        tree = html.fromstring(driver.page_source)

        try:
            product_name = tree.xpath("//div[@class='DrugHeader__left___19WY-']/h1/text()")[0]
        except:
            continue

        try:
            feedback = get_feedback(tree)
        except:
            feedback = {}

        # FAQs

        try:
            faq = get_faq(tree)
        except:
            faq = []

        # Patient Concerns

        try:
            patient_concerns = get_patient_concerns(tree)
        except:
            patient_concerns = []

        # Side Effects

        try:
            side_effects = get_side_effects(tree)
        except:
            side_effects = []


        prod_data = {
            "product_name": product_name,
            "feedback": feedback,
            "faq": faq,
            "patient_concerns": patient_concerns,
            "side_effects": side_effects
        }

        drug_data.append(prod_data)

        with open(f"./store/{drug}_{i}.json",'w') as f:
            # f.write(json.dumps(prod_data))
            json.dump(prod_data, f, indent=4)


    drugs_data[drug] = drug_data


with open("data.json", "w") as f:
    json.dump(drugs_data, f)

driver.quit()
