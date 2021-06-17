
products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
]

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}"


# 1) capture product IDs until done using infinite loop with data input validation

selected_ids = []

valid_ids_range = range(1,21)
valid_ids = [str(id) for id in valid_ids_range]

while True: 
    
    selected_id = input("Please select / scan a valid product id: ")
    if selected_id.upper() == "DONE":
        break
    else:      
        if selected_id in valid_ids:
            selected_ids.append(selected_id)
        else:
            print("Hey, are you sure that product identifier is correct? Please try again!")
    

# 2) print receipt header including timestamp 

import datetime
now = datetime.datetime.now()

print("---------------------------------")
print("GREEN FOODS GROCERY")
print("WWW.GREEN-FOODS-GROCERY.COM")
print("---------------------------------")
print("CHECKOUT AT: "+now.strftime("%Y-%m-%d %I:%M %p"))
print("---------------------------------")
print("SELECTED PRODUCTS:")


# 3) perform product lookups to determine the product's name and price and compute subtotal 

subtotal = 0

for selected_id in selected_ids:
    matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
    matching_product = matching_products[0]
    print("... "+matching_product["name"]+" ("+to_usd(matching_product["price"])+")")
    subtotal = subtotal + (float(matching_product["price"]))


# 4) prints the subtotal, tax, and total using the .env file varialbe

import os
import dotenv

dotenv.load_dotenv()

tax_rate = float(os.getenv("TAX_RATE"))

print("---------------------------------")
print(f"SUBTOTAL: {to_usd(subtotal)}")
print(f"TAX: {to_usd(subtotal*tax_rate)}")
print(f"TOTAL: {to_usd(subtotal*(1+tax_rate))}")
print("---------------------------------")
print("THANKS, SEE YOU AGAIN SOON!")
print("---------------------------------")


# 5) send email receipt


cust_consent = input("Does the customer want an email receipt (yes or no): ")
if cust_consent.upper() == "YES":       
    cust_email = input("Please input email address: ")

    current_time = now.strftime("%Y-%m-%d %I:%M %p")
    total = to_usd(subtotal*(1+tax_rate))

    products_list = []
    for selected_id in selected_ids:
        empty_dict = {}
        empty_dict["id"] = int(selected_id)
        matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
        matching_product = matching_products[0]
        empty_dict["name"] = matching_product["name"]
        products_list.append(empty_dict)
        
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
    SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
    SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")

    template_data = {
        "total_price_usd": total,
        "human_friendly_timestamp": current_time,
        "products": products_list
    }

    client = SendGridAPIClient(SENDGRID_API_KEY)

    message = Mail(from_email=SENDER_ADDRESS, to_emails=cust_email)
    message.template_id = SENDGRID_TEMPLATE_ID
    message.dynamic_template_data = template_data

    try:
        response = client.send(message)
        print("RESPONSE:", type(response))
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as err:
        print(type(err))
        print(err)