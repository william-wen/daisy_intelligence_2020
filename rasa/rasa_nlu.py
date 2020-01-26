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
    unit, save, percent, quantity, cost = [], [], [], [], []
    list_of_units = ["lb", "pound", "bag", "can", "capsule", "g", "mg", "milligrams", "kg", "gallon", "gal", "liter", "l", "ml", "oz", "ounce", "pack", "package", "pint", "pt", "quart", "qt", "serving", "tablet", "inch", "\"", "dozen", "cup", "cups", "c", "piece"]
    for line in all_lines:   
        response = loop.run_until_complete(model.parse_message_using_nlu_interpreter(line))
        entities = response["entities"]

        unit += [entity["value"] for entity in entities if entity["entity"] == "unit"]
        percent += [entity["value"] for entity in entities if entity["entity"] == "percent"]
        quantity += [entity["value"] for entity in entities if entity["entity"] == "quantity"]

        if response["intent"]["name"] == "save" or response["intent"]["name"] == "price":
            save.append(response["text"])

    done_items = {
        "unit": unit,
        "percent": percent,
        "quantity": quantity,
    }

    # $14.99 or cents/lb
    reg_cost1 = "".join((
        r"(?P<cost>(\$[\d\.\,]+|[\d\.\,]+\¢))\/(?P<unit>.*)"
    ))

    # 2/$15 or cents
    reg_cost2 = "".join((
        r"(?P<quantity>\d)+\/(?P<cost>(\$[\d\.\,]+)|[\d\.\,]+\¢)"
    ))

    # SAVE $1/1¢ on 4
    reg_save1 = "".join((
        r"(?i)save\s(?P<save>(\$[\d\.\,]+)|[\d\.\,]+\¢)\s(?i)on\s(?P<quantity>\d)+"
    ))

    # SAVE ($5 | 5¢)
    reg_save2 = "".join((
        r"(?i)save\s*\$*(?P<save>(\$[\d\.\,]+)|[\d\.\,]+\¢)"
    ))

    save_processed, cost_processed = [], []
    print(save)

    for cost_items in cost:
        if re.search(reg_cost1, cost_items):
            match = re.search(reg_cost1, cost_items)
            cost_processed.append(match.group("cost"))
            unit.append(match.group("unit"))
        
        if re.search(reg_cost2, cost_items):
            match = re.search(reg_cost2, cost_items)
            cost_processed.append(match.group("cost"))
            quantity.append(match.group("quantity"))

    for save_items in save:
        if re.search(reg_save1, save_items):
            match = re.search(reg_save1, save_items)
            save_processed.append(match.group("save"))
            quantity.append(match.group("quantity"))
        
        if re.search(reg_save2, save_items):
            match = re.search(reg_save2, save_items)
            save_processed.append(match.group("save"))
    
    done_items["cost"] = cost_processed
    done_items["save"] = save_processed
    done_items["quantity"] = quantity

    print(done_items)