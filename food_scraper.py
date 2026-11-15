
# Importing necessary libraries:
import requests
import numpy as np
import pandas as pd
from time import sleep

# Defining a class for scraping food information:
class Scraper():

    def __init__(self, url) -> None:
        # Initializing the class with the website URL:
        self.url = url

        # Initializing a dictionary to store the scraped food information:
        self.params = dict(
            name=[],
            brand=[],
            barcode=[],
            calories=[],
            proteins=[],
            carbohydrates=[],
            fat=[],
            sugar=[],
            salt=[],
        )

        # Setting the number of pages to scrape:
        self.pages_list = 5

        # Initializing the page number to start scraping:
        self.page_num = 1

        # Defining the request headers:
        self.headers = {
            "User-Agent": "FoodNutritionStudentProject/1.0 (educational use)"
        }

    def main(self):
        # Looping through each page to scrape food information:
        for i in range(self.pages_list):
            print(f"\nPage num: {self.page_num}")

            # Getting all food products from the current page:
            products = self.get_food_products()

            # Looping through each product to extract its information:
            for product in products:
                try:
                    self.get_food_info(product)
                except Exception as e:
                    # Printing the error and continuing to the next product:
                    print(f"Product extraction error: {e}")
                    continue

            # Displaying the number of products found on the current page:
            print(f"Products extracted: {len(products)}")

            # Incrementing the page number to move to the next page:
            self.page_num += 1

            # Waiting 2 seconds before requesting the next page:
            sleep(2)

        # Returning the dictionary containing all scraped information:
        return self.params

    def get_food_products(self):
        # Defining the API URL:
        url = self.url + "/api/v2/search"

        # Defining the search parameters:
        params = {
            "categories_tags_en": "sweets",
            "page": self.page_num,
            "page_size": 20,
            "fields": "code,product_name,brands,nutriments,quantity"
        }

        # Trying to retrieve the products up to 3 times:
        for attempt in range(3):
            try:
                print(f"Request attempt: {attempt + 1}")

                # Sending a GET request to the website:
                response = requests.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=30
                )

                # Checking if the request was successful:
                response.raise_for_status()

                # Converting the response into JSON format:
                data = response.json()

                # Extracting the list of food products:
                products = data.get("products", [])

                print(f"Found {len(products)} products")

                # Returning the list of products:
                return products

            except requests.exceptions.RequestException as e:
                # Printing the request error:
                print(f"Request error: {e}")

                # Waiting before trying the request again:
                if attempt < 2:
                    wait_time = 5 * (2 ** attempt)
                    print(f"Waiting {wait_time} seconds...")
                    sleep(wait_time)

        # Returning an empty list if all attempts fail:
        print("Unable to retrieve this page.")
        return []

    def get_food_info(self, product):
        # Getting the food name:
        try:
            name = product.get("product_name", np.nan)
        except:
            name = np.nan

        # Getting the food brand:
        try:
            brand = product.get("brands", np.nan)
        except:
            brand = np.nan

        # Getting the product barcode:
        try:
            barcode = product.get("code", np.nan)
        except:
            barcode = np.nan

        # Getting the nutritional information of the product:
        nutrition = product.get("nutriments", {})

        # Extracting calories per 100 grams:
        try:
            calories = nutrition.get("energy-kcal_100g", np.nan)
        except:
            calories = np.nan

        # Extracting proteins per 100 grams:
        try:
            proteins = nutrition.get("proteins_100g", np.nan)
        except:
            proteins = np.nan

        # Extracting carbohydrates per 100 grams:
        try:
            carbohydrates = nutrition.get("carbohydrates_100g", np.nan)
        except:
            carbohydrates = np.nan

        # Extracting fats per 100 grams:
        try:
            fat = nutrition.get("fat_100g", np.nan)
        except:
            fat = np.nan

        # Extracting sugars per 100 grams:
        try:
            sugar = nutrition.get("sugars_100g", np.nan)
        except:
            sugar = np.nan

        # Extracting salt per 100 grams:
        try:
            salt = nutrition.get("salt_100g", np.nan)
        except:
            salt = np.nan



        # Adding the extracted information to the dictionary:
        self.params["name"].append(name)
        self.params["brand"].append(brand)
        self.params["barcode"].append(barcode)
        self.params["calories"].append(calories)
        self.params["proteins"].append(proteins)
        self.params["carbohydrates"].append(carbohydrates)
        self.params["fat"].append(fat)
        self.params["sugar"].append(sugar)
        self.params["salt"].append(salt)


# Running the scraper:
basic_url = "https://world.openfoodfacts.org"
scraper = Scraper(basic_url)
params = scraper.main()

# Creating a range of indexes for the scraped products:
i = range(1, len(params["name"]) + 1)

# Converting the scraped information into a DataFrame:
df = pd.DataFrame(params, index=i)

# Displaying the scraped food information:
print("\nScraped food information:")
print(df)

# Exporting the scraped information into a CSV file:
df.to_csv("food_nutrition_scraping.csv", index=False)

print("\nFood scraping completed successfully!")
print(f"Total products extracted: {len(df)}")
print("File saved: food_nutrition_scraping.csv")
