import pandas as pd
import re
from fuzzywuzzy import process, fuzz

obj = {
    "cost":["$5"],
    "save":["$6.98"],
    "quantity":["2"],
    "percent":[],
    "unit":["1 Pint"]
}

##### TEST VALUES:
unit_promo_price = calculate_unit_promo_price(
    obj["cost"],
    obj["quantity"]
)

uom = obj["unit"]

least_unit_for_promo = calculate_least_unit_for_promo(
    obj["save"],
    obj["quantity"]
)

save_per_unit = "Save $3.5 on 2"
discount = "2/$5"

products = list(pd.read_csv("product_dictionary.csv")["product_name"])
products.sort(key=len, reverse=True)

columns = [
    "flyer_name",
    "product_name",
    "unit_promo_price",
    "uom",
    "least_unit_for_promo",
    "save_per_unit",
    "discount",
    "organic"
]

df = pd.DataFrame(columns=columns)
flyer_name = process.extract("Boston Butt Pork Roast and Boneless", products)

# looping through line by line
for i in range(8):
#     flyer_name = re.findall("\#.*\#", )[0]
    choices = process.extract("Boston Butt Pork Roast and Boneless", products)

    # Tentative:
    prod_names = [name for name, num in choices]
    prod_names.sort(key=len, reverse=True)
    flyer_name = prod_names[0]

    if re.search(r"(?i)organic", flyer_name):
        organic = 1
    else:
        organic = 0

    df.loc[i] = [
        flyer_name,
        2,
        3,
        4,
        5,
        6,
        7,
        8
    ]

# 2/$5
def calculate_unit_promo_price(cost, quant):
    cost = cost.replace("$", "").replace(" ", "").strip()

    try:
        cost = float(cost)
        return round(cost / float(quant.strip()), 2)

    except TypeError:
        return None

# Save $3 on 4
def calculate_least_unit_for_promo(quant):
    try:
        return float(quant.replace(" ", "").strip())

    except:
        return 1

# Save $3 on 4
def calculate_save_per_unit(string):
