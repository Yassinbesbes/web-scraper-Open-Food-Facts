## Project Description

This project is a web scraper written in Python using the requests, NumPy and pandas libraries. The purpose of the scraper is to extract nutritional information about sweets products from the Open Food Facts API. The scraped data includes various details about each product such as its name, brand, barcode, calories, proteins, carbohydrates, fat, sugar, salt, and serving size. The nutritional values are given per 100 g.

## Code Structure

The code is organized into the following sections:

- **Scraper Class**: This section defines the Scraper class and its constructor. The constructor initializes several variables such as the website URL to be scraped, a dictionary to store the scraped information, the number of pages to scrape, the page number to start scraping, and the request headers.
- **Main Method**: This section contains the main method that starts the scraping process. For each page, it calls the get_food_products method to retrieve all the products on that page. Then, for each product, it calls the get_food_info method to extract the product's information and add it to the dictionary of scraped information. The method waits for two seconds between pages.
- **get_food_products Method**: This section defines the get_food_products method that sends a request to the Open Food Facts API and retrieves the list of sweets products for a given page. Each page contains 20 products.
- **get_food_info Method**: This section defines the get_food_info method that extracts information from a single product, including its name, brand, barcode, calories, proteins, carbohydrates, fat, sugar, salt, and serving size. If a value is missing, it is stored as NaN.
- **Error Handling**: If a request fails, the scraper retries up to three times, waiting 5 seconds and then 10 seconds between attempts. If all attempts fail, the page is skipped. If an error occurs while extracting a product, the product is skipped and the scraper continues with the next one.
- **Returned Data**: The main method returns a dictionary where each key is a field name and each value is a list containing that field for all scraped products. This dictionary is then converted into a pandas DataFrame and saved as a CSV file named food_nutrition_scraping.csv.

## Usage

To use this scraper, install the required libraries, then run the script:

```
pip install requests numpy pandas
python scraper.py
```

The scraped data will be saved in the file food_nutrition_scraping.csv.

## Notes

The serving_size column may be mostly empty because this field is not included in the fields parameter of the API request. To fill it, add serving_size to that parameter in the get_food_products method.
