#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import subprocess
import json

class ALFood(object):
    def __init__(self, session):
        self.session = session

    def get_cocktail_info(self):
        url =  "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        command = ["curl", "-k", url]
        try:
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = result.communicate()
            if result.returncode == 0:
                cocktail_data = json.loads(output)
                return cocktail_data
            else:
                print("Erreur :", error)
        except Exception as e:
            print("Erreur lors de l'exécution de la commande :", e)


    def extract_cocktail_data(self, cocktail_data):
        if cocktail_data and "drinks" in cocktail_data:
            drinks = cocktail_data["drinks"]
            if drinks and len(drinks) > 0:
                return drinks[0]  # Retourne le premier cocktail
        return None


    def get_meal_info(self):
        url =  "https://www.themealdb.com/api/json/v1/1/random.php"
        command = ["curl", "-k", url]
        try:
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = result.communicate()
            if result.returncode == 0:
                meal_data = json.loads(output)
                return meal_data
            else:
                print("Erreur :", error)
        except Exception as e:
            print("Erreur lors de l'exécution de la commande :", e)


    def extract_meal_data(self, meal_data):
        if meal_data and "meals" in meal_data:
            meals = meal_data["meals"]
            if meals and len(meals) > 0:
                return meals[0]  # Retourne le premier meal
        return None
    
    def getCocktail(self):
        tablet_service = self.session.service("ALTabletService")
        tablet_service.cleanWebview()
        tablet_service.enableWifi()

        # Obtenir les informations sur un cocktail
        cocktail_data = self.get_cocktail_info()
        cocktail_info = self.extract_cocktail_data(cocktail_data)

        if cocktail_info:
            print("\nCocktail infos :\n")
            print(cocktail_info['strDrinkThumb'])
            tablet_service.showWebview(cocktail_info['strDrinkThumb'])
            tts = self.session.service("ALTextToSpeech")
            tts.setLanguage("English")
            tts.say(cocktail_info['strDrink'])
            tts.say(cocktail_info['strInstructions'])

    def getMeal(self):
        tablet_service = self.session.service("ALTabletService")
        tablet_service.cleanWebview()
        tablet_service.enableWifi()

        meal_data = self.get_meal_info() 
        meal_info = self.extract_meal_data(meal_data)

        if meal_info:
            print("\n Meals infos :\n")
            print(meal_info['strMealThumb'])
            tablet_service.showWebview(meal_info['strMealThumb'])
            tts = self.session.service("ALTextToSpeech")
            tts.setLanguage("English")
            tts.say(meal_info['strMeal'])
            tts.say(meal_info['strInstructions'])