import pandas as pd
import re
from fuzzywuzzy import process, fuzz

# 2/$5
def calculate_unit_promo_price(cost, quant):
    if cost:
        cost = cost[0].replace("$", "").replace(" ", "").strip()
    else:
        return None

    try:
        cost = float(cost)
        if quant and float(quant[0].strip()) != 0:
            return round(cost / float(quant[0].strip()), 2)
        else:
            return None

    except ValueError:
        return None

# Save $3 on 4
def calculate_least_unit_for_promo(quant):
    try:
        return float(quant[0].replace(" ", "").strip())

    except:
        return 1

# Save $3 on 4
def calculate_save_per_unit(save, quant):
    if save:
        save = save[0].replace("$", "").replace(" ", "").strip()
    return None

    try:
        save = float(save)
        if quant and float(quant[0].strip()) != 0:
            return round(save / float(quant[0].strip()), 2)
        else:
            return None

    except ValueError:
        return None

def calculate_discount(save, cost, percentage):
    try:
        if percentage:
            percentage = percentage[0].replace(" ", "").strip()
            return round((float(percentage)/100), 2)

        if save:
            save = save[0].replace("$", "").strip()
        else:
            return None

        if cost:
            cost = cost[0].replace("$", "").strip()
        else:
            return None

        save = float(save)
        cost = float(save)

        if save+cost != 0:
            return round(float(save/(save+cost)), 2)
    except ValueError:
        return None

def process_csv(obj, row_num, df):

    cost, save, quantity, percent, unit = obj["cost"], obj["save"], obj["quantity"], obj["percent"], obj["unit"]

    unit_promo_price = calculate_unit_promo_price(
        cost,
        quantity
    )

    uom = unit

    least_unit_for_promo = calculate_least_unit_for_promo(
        quantity
    )

    save_per_unit = calculate_save_per_unit(
        save,
        quantity
    )

    discount = calculate_discount(
        save,
        cost,
        percent
    )

    products = list(pd.read_csv("../product_dictionary.csv")["product_name"])
    products.sort(key=len, reverse=True)

    product_name = process.extract(obj["string_block"], products)
    # print("PRODUCT NAMEEEEEEEE:        " + str(product_name))

    if product_name:
        if product_name[0][1] < 50:
            prod_name = None
        else:
            prod_name=product_name[0][0]
    # prod_name = product_name[0]
    # print(prod_name)

    if prod_name is not None:
        if re.search(r"(?i)organic", prod_name):
            organic = 1
        else:
            organic = 0
    else:
        organic = 0

    df.loc[row_num] = [
        obj["flyer_name"],
        prod_name,
        unit_promo_price,
        uom,
        least_unit_for_promo,
        save_per_unit,
        discount,
        organic
    ]

    return df

    
