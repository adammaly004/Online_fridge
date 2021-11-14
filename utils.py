import json
import os


def open_file(name, mode="r", data=None):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, name)

    if mode == "r":
        with open(file_path, mode, encoding='utf-8') as f:
            data = json.load(f)
            return data

    elif mode == "w":
        with open(file_path, mode, encoding='utf-8') as f:
            json.dump(data, f)


class Cook:
    def __init__(self, recipes, fridge):
        self.recipes = recipes
        self.fridge = fridge

    def check_resource(self):
        foods = []
        for recipe in self.recipes:
            index = 0
            for key, num in recipe["resource"].items():
                if self.fridge.get(key) and num <= self.fridge.get(key):
                    index += 1
                    if index == len(recipe["resource"]):
                        foods.append(
                            {"name": recipe["name"], "procedure": recipe["procedure"]})

        return foods

    def update_fridge(self, food):
        index = 0
        for recipe in self.recipes:
            if recipe.get("name") == food:
                for res, num in self.recipes[index]["resource"].items():
                    self.fridge[res] = round(self.fridge[res] - num, 2)
            index += 1

        return self.fridge

    def add_item(self, item, num):
        if not item in self.fridge:
            self.fridge.update({item: int(num)})

        else:
            self.fridge[item] += int(num)

        return self.fridge

    def show_info(self, food):
        for recipe in self.recipes:
            if recipe.get("name") == food:
                return recipe
