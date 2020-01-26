import asyncio
import os
import re
from rasa.model import get_model
from rasa.core.agent import Agent

def load_model():
    """Loads rasa nlu models

    Args:
        model_dir: The model directory of the loaded model

    Returns:
        Returns the agent responsible for parsing text
    """
    ROOT = "models/"
    MODELS = ["{}{}".format(ROOT, file) for file in os.listdir(ROOT) if "nlu" in file]
    MODEL_PATH = sorted(MODELS, key=os.path.getctime, reverse=True)[0]
    get_interpreter = get_model(MODEL_PATH)

    return Agent.load(get_interpreter)


loop = asyncio.get_event_loop()
model = load_model()
file = 'test_text.txt'
with open(file, 'r') as file:
    all_lines = file.readlines()
    list_of_units = ["lb", "pound", "bag", "can", "capsule", "g", "mg", "milligrams", "kg", "gallon", "gal", "liter", "l", "ml", "oz", "ounce", "pack", "package", "pint", "pt", "quart", "qt", "serving", "tablet", "inch", "\"", "dozen", "cup", "cups", "c", "piece"]
    unit, save, percent_processed, quantity, cost = [], [], [], [], []
    percent = []
    # $14.99 or ¢
    reg_cost1 = "".join((
        r"(?P<cost>(\$[\d\.\,]+|[\d\.\,]+\¢))"
    ))

    # 2/$15 or cents
    reg_cost2 = "".join((
        r"(?P<quantity>\d)+\/(?P<cost>(\$[\d\.\,]+)|[\d\.\,]+\¢)"
    ))

    # $14.99 or ¢ / unit
    reg_cost3 = "".join((
        r"(?P<cost>(\$[\d\.\,]+|[\d\.\,]+\¢))\/(?P<unit>.*)"
    ))

    # SAVE $1/1¢ on 4
    reg_save1 = "".join((
        r"(?i)save\s(?P<save>(\$[\d\.\,]+)|[\d\.\,]+\¢)\s(?i)on\s(?P<quantity>\d)+"
    ))

    # SAVE ($5 | 5¢)
    reg_save2 = "".join((
        r"(?i)save\s*\$*(?P<save>(\$[\d\.\,]+)|[\d\.\,]+\¢)"
    ))

    # save $14.99 or ¢ / unit
    reg_save3 = "".join((
        r"(?i)save\s(?P<save>(\$[\d\.\,]+|[\d\.\,]+\¢))\/(?P<unit>.*)"
    ))

    # $5 Off
    reg_save4 = "".join((
        r"(?P<save>(\$[\d\.\,]+)|[\d\.\,]+\¢)\s(?i)off"
    ))

    # 20% off
    reg_percent1 = "".join(
        r"(?P<percent>[\d\.\,]+)\%\s(?i)off"
    )


    for line in all_lines:  
        if "#####" in line or line is all_lines[-1]:
            response = loop.run_until_complete(model.parse_message_using_nlu_interpreter(line))
            entities = response["entities"]

            unit += [entity["value"] for entity in entities if entity["entity"] == "unit"]
            percent += [entity["value"] for entity in entities if entity["entity"] == "percent"]
            quantity += [entity["value"] for entity in entities if entity["entity"] == "quantity"]

            if response["intent"]["name"] == "save":
                save.append(response["text"])

            if response["intent"]["name"] == "price":
                cost.append(response["text"])

            for unit_items in list(unit):
                unit_items_array = unit_items.lower().replace(".", "").split()
                if not any(a == b for a in unit_items_array for b in list_of_units):
                    unit.remove(unit_items)
                    
            # percent_processed is not necessary because rasa already does a good job detecting percents
            save_processed, cost_processed = [], []
            for cost_items in cost:
                if re.search(reg_cost3, cost_items):
                    match = re.search(reg_cost3, cost_items)
                    print("hello")
                    cost_processed.append(match.group("cost"))
                    unit.append(match.group("unit"))

                elif re.search(reg_cost2, cost_items):
                    match = re.search(reg_cost2, cost_items)
                    cost_processed.append(match.group("cost"))
                    quantity.append(match.group("quantity"))

                elif re.search(reg_cost1, cost_items):
                    match = re.search(reg_cost1, cost_items)
                    cost_processed.append(match.group("cost"))

            for save_items in save:
                if re.search(reg_save3, save_items):
                    match = re.search(reg_save3, save_items)
                    save_processed.append(match.group("save"))
                    unit.append(match.group("unit"))

                elif re.search(reg_save1, save_items):
                    match = re.search(reg_save1, save_items)
                    save_processed.append(match.group("save"))
                    quantity.append(match.group("quantity"))
                
                elif re.search(reg_save2, save_items):
                    match = re.search(reg_save2, save_items)
                    save_processed.append(match.group("save"))
                
                elif re.search(reg_save4, save_items):
                    match = re.search(reg_save4, save_items)
                    save_processed.append(match.group("save"))

            for percent_items in percent:
                if re.search(reg_percent1, percent_items):
                    match = re.search(reg_percent1, percent_items)
                    percent_processed.append(match.group("percent"))

            done_items = {
                "cost": list(set(cost_processed)),
                "save": list(set(save_processed)),
                "quantity": list(set(quantity)),
                "percent": list(set(percent_processed)),
                "unit": list(set(unit))
            }

            print(done_items)

            unit, save, percent, quantity, cost = [], [], [], [], []
            save_pocessed, cost_processed, percent_processed = [], [], []
            # use information in done items to calculate the other columsn

            # find what the product name is
        else: 
            response = loop.run_until_complete(model.parse_message_using_nlu_interpreter(line))
            entities = response["entities"]

            unit += [entity["value"] for entity in entities if entity["entity"] == "unit"]
            percent_processed += [entity["value"] for entity in entities if entity["entity"] == "percent"]
            quantity += [entity["value"] for entity in entities if entity["entity"] == "quantity"]

            if response["intent"]["name"] == "save":
                save.append(response["text"])

            if response["intent"]["name"] == "price":
                cost.append(response["text"])

            if response["intent"]["name"] == "percent":
                percent.append(response["text"])