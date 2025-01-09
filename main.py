import streamlit as st
import sqlite3
from datetime import datetime
import csv
from PIL import Image
import pandas as pd

# -------------------------------- DATABASE -------------------------------- #
# Initialize database
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Create table for orders if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization TEXT,
    meal_category TEXT,
    selected_meals TEXT,
    number_of_people INTEGER,
    total_cost REAL,
    total_selling_price REAL,
    contribution_margin REAL,
    cost_margin REAL,
    date TEXT,
    day_of_week TEXT
)
""")
conn.commit()

# Predefined meals and categories
MEAL_CATEGORIES = {
"Complementary Breakfast": [
    ("TOASTED BREAD", 500.00, 1000),
    ("AMERICAN PANCAKE", 1547, 3100),
    ("BOILED YAM", 508, 3000),
    ("FRIED NOODLES", 1201, 3000),
    ("CORN PAP", 468, 2000),
    ("WATERMELON", 200, 500),
    ("ORANGE FRUIT", 100, 500),
    ("BAKED BEANS", 895, 2000),
    ("PUFF-PUFF", 200, 600),
    ("MINI SANDWICH", 300, 600),
    ("BOILED SWEET POTATO", 910, 3000),
    ("STIR FRY PASTA", 1344, 3500),
    ("SUNNY SIDE UP", 747, 2000),
    ("CUSTARD", 442, 2000),
    ("MOI-MOI", 1368, 3000),
    ("PAW-PAW", 250, 500),
    ("BREAD ROLLS", 500, 1000),
    ("WAFFLES", 500, 1000),
    ("OVEN BAKED POTATO", 1764, 3000),
    ("JOLLOF MACCARONI", 800, 3000),
    ("ACHA PUDDING", 1100, 2500),
    ("WATERMELON JUICE", 500, 1000),
    ("SWEET MELON", 400, 1000),
    ("PINEAPPLE", 400, 1000),
    ("SWEET POTATO NUGGET", 910, 3000),
    ("FRESH BREAD", 250, 1000),
    ("BOILED POTATO", 910, 3000),
    ("SPAGHETTI JOLLOF", 777, 3000),
    ("OPEN SANDWICH", 2500, 5000),
    ("NIGERIAN PANCAKE", 1000, 2000),
    ("FRIED SWEET POTATO", 400, 3000),
    ("MASA", 400, 3000),
    ("JOLLOF RICE", 800, 3000),
    ("VEGETABLE SAUCE", 1100, 3000),
    ("GERMAN PANCAKE", 1200, 2500),
    ("GOLDEN YAM", 844, 3500),
    ("OAT", 400, 2000),
    ("EGG SANDWICH", 2000, 6000),
    ("YAM CHIPS", 800, 3000),
    ("VEGETABLE NOODLES", 1500, 3000),
    ("FRITATA", 1500, 3000),
    ("STIRFRY MACCARONI", 1200, 3000),
    ("BEANS POTTAGE", 800, 3000),
    ("INFUSED WATER", 878.60, 2000),
    ("EWEDU SOUP", 772.38, 2000),
    ("EFORIRO SOUP", 2357.28, 3500),
    ("KUKA SOUP", 798.18, 2000),
    ("WAFFLES", 226.20, 1000),
    ("SLICED CAKE", 130.51, 500),
    ("FRUITE CAKE", 1804.23, 4000),
    ("TEA BAG", 117, 150),
    ("COFFEE", 150, 300),
    ("CHOCOLATE", 200, 400),
    ("HONEY", 50, 100),
    ("SUGAR", 26, 50),
    ("CORNFLAKES", 200, 2000),
    ("BROWN SUGAR", 5, 50),
    ("COCO POPS", 150, 2000),
    ("RICE CRISPIES", 500, 2000),
    ("BUTTER", 100, 200),
    ("PANCAKE SYRUP", 100, 150),
    ("MINI SANDWICH", 600, 1200),
    ("SWEET POTATO NUGGET", 910, 3000),
    ("YAM CHIPS", 800, 1000),
    ("CHICKEN", 1650, 4500),
    ("SPAGHETTI JOLLF", 777, 3000),
    ("BOILED YAM", 508, 3000),
    ("EGG SAUCE", 760, 3000),
    ("SCRAMBLED EGG", 770, 2000),
    ("TOMATO SAUCE", 500, 1000),
    ("FISH SAUCE", 2100, 5000),
    ("KIDNEY SAUCE", 2300, 3000),
    ("LIVER SAUCE", 1400, 3000),
    ("BEEF STEW", 1400, 4000),
    ("CHICKEN STEW", 1800, 5000),
    ("AKARA", 960, 2000),
    ("STEAMED VEG", 500, 2000),
    ("WATER 75CL", 137, 700),
    ("SAUSAGE", 425, 1200),
    ("CHICKEN PIE", 350, 1400),
    ("APPLE", 400, 1000),
    ("VEGETABLE NOODLES", 1500, 6000),
    ("MILK", 115, 300)
],
"AM Tea Break": [
    ("TEA BAG", 117, 150),
    ("COFFEE", 150, 300),
    ("CHOCOLATE", 200, 400),
    ("HONEY", 50, 100),
    ("SUGAR", 26, 50),
    ("CORNFLAKES", 200, 2000),
    ("BROWN SUGAR", 5, 50),
    ("COCO POPS", 150, 2000),
    ("RICE CRISPIES", 500, 2000),
    ("TOASTED BREAD", 1000),
    ("BUTTER", 100, 200),
    ("AMERICAN PANCAKE", 1547, 3500),
    ("MINI SANDWICH", 600, 5000),
    ("PUFF-PUFF", 300, 600),
    ("BREAD ROLLS", 500, 1000),
    ("WAFFLES", 500, 1000),
    ("SWEET POTATO NUGGET", 910, 3000),
    ("FRESH BREAD", 250, 1000),
    ("OPEN SANDWICH", 2500, 5000),
    ("NIGERIAN PANCAKE", 700, 2000),
    ("EGG SANDWICH", 2000, 6000),
    ("YAM CHIPS", 800, 3000),
    ("GOLDEN YAM", 844, 3000),
    ("STIR FRY MACCARONI", 1200, 3000),
    ("FRIED SWEET POTATO", 400, 3000),
    ("MASA", 400, 3000),
    ("CHICKEN", 1650, 4500),
    ("JOLLOF RICE", 800, 3000),
    ("BOILED POTATO", 910, 3000),
    ("SPAGHETTI JOLLOF", 777, 3000),
    ("OVEN BAKED POTATO", 1764, 3000),
    ("JOLLOF MACCARONI", 800, 3000),
    ("BOILED SWEET POTATO", 910, 3000),
    ("STIR FRY PASTA", 1344, 3500),
    ("BOILED YAM", 508, 3000),
    ("FRIED NOODLES", 1201, 3000),
    ("EGG SAUCE", 760, 3000),
    ("SCRAMBLED EGG", 770, 2000),
    ("TOMATO SAUCE", 500, 1000),
    ("FISH SAUCE", 2100, 5000),
    ("KIDNEY SAUCE", 2300, 3000),
    ("VEGETABLE SAUCE", 1100, 3000),
    ("BOILED EGG", 400, 1500),
    ("LIVER SAUCE", 2400, 3000),
    ("BEEF STEW", 1400, 4000),
    ("CHICKEN STEW", 1800, 5000),
    ("FRITATA", 1500, 3000),
    ("ACHA PUDDING", 1100, 2500),
    ("AKARA", 960, 2000),
    ("OAT", 400, 2000),
    ("BEANS POTTAGE", 800, 3000),
    ("CORN PAP", 468, 3000),
    ("MOI-MOI", 1368, 3000),
    ("CUSTARD", 442, 2000),
    ("MINI SANDWICH", 300, 2500),
    ("SUNNY SIDE UP", 747, 1500),
    ("INFUSED WATER", 500, 2500),
    ("PAW-PAW", 250, 1000),
    ("WATERMELON JUICE", 500, 1000),
    ("SWEET MELON", 400, 1000),
    ("PINEAPPLE", 400, 1000),
    ("WATERMELON", 250, 1000),
    ("PAW-PAW FRUIT CUT", 500, 1500),
    ("ORANGE", 250, 500),
    ("BAKED BEANS", 895, 1000),
    ("STEAMED VEG", 500, 2000),
    ("WATER 75CL", 137, 700),
    ("SAUSAGE", 425, 1200),
    ("GERMAN PANCAKE", 1200, 3000),
    ("CHICKEN PIE", 350, 1400),
    ("APPLE", 400, 1000),
    ("VEGETABLE NOODLES", 1500, 6000),
    ("MILK", 115, 300),
    ("STIRFRY MACCARONI", 1200, 3000)
],
    "Buffet Lunch": [
    ("COCONUT RICE", 1300, 3000),
    ("CAT FISH", 1900, 4500),
    ("JOLLOF RICE", 800, 3000),
    ("MACARONI JOLLOF", 800, 3000),
    ("SEMO", 300, 1000),
    ("OHA", 1710, 3000),
    ("EGUSI", 1700, 3000),
    ("MACKEREL FISH", 1900, 4500),
    ("MEXICAN FRIED RICE", 2000, 5000),
    ("SNOW RICE", 900, 3500),
    ("STIRFRY PASTA", 1400, 3000),
    ("WHEAT", 400, 1000),
    ("EBA", 300, 1000),
    ("OGBONO", 1800, 3000),
    ("EWEDU", 1500, 3000),
    ("TOMATO STEW", 600, 2000),
    ("BEEF", 1270, 3500),
    ("VEGETABLE SALAD", 1400, 4000),
    ("CHINESE FRIED RICE", 2400, 5000),
    ("PASTA JOLLOF", 777, 3000),
    ("FRESH OKRO", 1310, 3000),
    ("CHICKEN", 1650, 4500),
    ("STEAMED VEGETABLE", 800, 2000),
    ("ENGLISH FRIED RICE", 2000, 5000),
    ("SNOW PASTA", 600, 3000),
    ("EFORIRO", 800, 3000),
    ("GREEN VEGETABLE SAUCE", 1400, 3000),
    ("CURRY FRIED RICE", 1900, 5000),
    ("VEGETABLE SOUP", 1600, 3000),
    ("BITTERLEAF", 1800, 3000),
    ("SNOW MACARONI", 600, 3000),
    ("PILAF RICE", 1900, 5000),
    ("VEGETABLE FRIED RICE", 3100, 5000),
    ("KUKA", 640, 2000),
    ("FRUIT IN SEASON", 250, 1000),
    ("MACKEREL FISH", 1800, 4500),
    ("CHICKEN", 1700, 4500),
    ("FRUIT PLATTER", 700, 2000),
    ("BEEF", 1300, 3500),
    ("NIGERIAN FRIED RICE", 859, 3000),
    ("FRESH FISH PEPPER SOUP", 2100, 5000),
    ("CORN AND CHICKEN SOUP", 1113, 3000),
    ("GOAT MEAT PEPPER SOUP", 1600, 5000),
    ("CHICKEN PEPPER SOUP", 1700, 6000),
    ("CHICKEN MINISTRONI", 1400, 3500),
    ("CREAM OF MUSHROOM SOUP", 1300, 3000),
    ("CREAM OF CHICKEN SOUP", 1200, 3000),
    ("GOLDEN YAM", 844, 3000),
    ("YAM PORRIDGE", 1500, 3000),
    ("MASHED POTATOES", 1720, 4000),
    ("FINGER FRIED YAM", 1200, 3000),
    ("HAND CUT FRIES", 2000, 4000),
    ("OVEN BAKED POTATOES", 1764, 3000),
    ("VANILLA SLICED CAKE", 600, 1500),
    ("CHOCOLATE SLICED CAKE", 870, 2000),
    ("FRUIT PLATTER", 650, 2000),
    ("FRUIT CAKE", 900, 2000),
    ("WATER 75CL", 137, 700),
    ("COWLEG PEPPER SOUP", 1800, 5500),
    ("BREAD ROLL", 500, 1000),
    ("FRUIT IN SEASON", 250, 1000),
    ("MOI-MOI", 1368, 3000),
    ("SNOW RICE", 900, 3000),
    ("WHITE BEANS", 773, 3000),
    ("MACKEREL FISH", 1800, 5000),
    ("BEEF", 1270, 3500),
    ("JOLLOF", 800, 3000),
    ("GOAT", 1400, 4500),
    ("DRY FISH", 1000, 6000),
    ("CAT FISH", 1900, 4500),
    ("FRIED PLANTAIN", 824, 3000),
    ("CHINESE FRIED RICE", 2400, 5000),
    ("RUSSIAN SALAD", 1710, 5000),
    ("WATER MELON", 200, 1000),
    ("WATER 75CL", 137, 700),
    ("SARDINE", 900, 2500)
],
    "AM Tea Break": [
    ("TEA BAG", 117, 150),
    ("COFFEE", 150, 300),
    ("CHOCOLATE", 200, 400),
    ("HONEY", 50, 100),
    ("SUGAR", 26, 50),
    ("CORNFLAKES", 200, 2000),
    ("BROWN SUGAR", 5, 50),
    ("COCO POPS", 150, 2000),
    ("RICE CRISPIES", 500, 2000),
    ("TOASTED BREAD", 1000),
    ("BUTTER", 100, 200),
    ("AMERICAN PANCAKE", 1547, 3500),
    ("MINI SANDWICH", 600, 5000),
    ("PUFF-PUFF", 300, 600),
    ("BREAD ROLLS", 500, 1000),
    ("WAFFLES", 500, 1000),
    ("SWEET POTATO NUGGET", 910, 3000),
    ("FRESH BREAD", 250, 1000),
    ("OPEN SANDWICH", 2500, 5000),
    ("NIGERIAN PANCAKE", 700, 2000),
    ("EGG SANDWICH", 2000, 6000),
    ("YAM CHIPS", 800, 3000),
    ("GOLDEN YAM", 844, 3000),
    ("STIR FRY MACCARONI", 1200, 3000),
    ("FRIED SWEET POTATO", 400, 3000),
    ("MASA", 400, 3000),
    ("CHICKEN", 1650, 4500),
    ("JOLLOF RICE", 800, 3000),
    ("BOILED POTATO", 910, 3000),
    ("SPAGHETTI JOLLOF", 777, 3000),
    ("OVEN BAKED POTATO", 1764, 3000),
    ("JOLLOF MACCARONI", 800, 3000),
    ("BOILED SWEET POTATO", 910, 3000),
    ("STIR FRY PASTA", 1344, 3500),
    ("BOILED YAM", 508, 3000),
    ("FRIED NOODLES", 1201, 3000),
    ("EGG SAUCE", 760, 3000),
    ("SCRAMBLED EGG", 770, 2000),
    ("TOMATO SAUCE", 500, 1000),
    ("FISH SAUCE", 2100, 5000),
    ("KIDNEY SAUCE", 2300, 3000),
    ("VEGETABLE SAUCE", 1100, 3000),
    ("BOILED EGG", 400, 1500),
    ("LIVER SAUCE", 2400, 3000),
    ("BEEF STEW", 1400, 4000),
    ("CHICKEN STEW", 1800, 5000),
    ("FRITATA", 1500, 3000),
    ("ACHA PUDDING", 1100, 2500),
    ("AKARA", 960, 2000),
    ("OAT", 400, 2000),
    ("BEANS POTTAGE", 800, 3000),
    ("CORN PAP", 468, 3000),
    ("MOI-MOI", 1368, 3000),
    ("CUSTARD", 442, 2000),
    ("MINI SANDWICH", 300, 2500),
    ("SUNNY SIDE UP", 747, 1500),
    ("INFUSED WATER", 500, 2500),
    ("PAW-PAW", 250, 1000),
    ("WATERMELON JUICE", 500, 1000),
    ("SWEET MELON", 400, 1000),
    ("PINEAPPLE", 400, 1000),
    ("WATERMELON", 250, 1000),
    ("PAW-PAW FRUIT CUT", 500, 1500),
    ("ORANGE", 250, 500),
    ("BAKED BEANS", 895, 1000),
    ("STEAMED VEG", 500, 2000),
    ("WATER 75CL", 137, 700),
    ("SAUSAGE", 425, 1200),
    ("GERMAN PANCAKE", 1200, 3000),
    ("CHICKEN PIE", 350, 1400),
    ("APPLE", 400, 1000),
    ("VEGETABLE NOODLES", 1500, 6000),
    ("MILK", 115, 300),
    ("STIRFRY MACCARONI", 1200, 3000)
],
    "Dinner": [
    ("COWLEG PEPPER SOUP", 1800, 5500),
    ("BREAD ROLL", 500, 1000),
    ("FRUIT IN SEASON", 250, 1000),
    ("MOI-MOI", 1368, 3000),
    ("SNOW RICE", 900, 3000),
    ("WHITE BEANS", 773, 3000),
    ("MACKEREL FISH", 1800, 5000),
    ("BEEF", 1270, 3500),
    ("JOLLOF", 800, 3000),
    ("GOAT", 1400, 4500),
    ("DRY FISH", 1000, 6500),
    ("CAT FISH", 1900, 4500),
    ("FRIED PLANTAIN", 824, 3000),
    ("CHINESE FRIED RICE", 2400, 5000),
    ("RUSSIAN SALAD", 1710, 5000),
    ("VANILLA SLICED CAKE", 409, 1500),
    ("SEMO", 300, 1000),
    ("EGUSI", 1700, 3000),
    ("FRESH OKRO", 1310, 3000),
    ("WHEAT", 400, 1000),
    ("OGBONO", 1720, 3000),
    ("EBA", 300, 1000),
    ("STEW", 600, 2000),
    ("CHICKEN", 1700, 4500),
    ("WATER MELON", 200, 1000),
    ("WATER 75CL", 137, 700),
    ("SARDINE", 900, 2500),
    ("COCONUT RICE", 1300, 3000),
    ("MACARONI JOLLOF", 800, 3000),
    ("OHA", 1710, 3000),
    ("MEXICAN FRIED RICE", 2000, 5000),
    ("STIRFRY PASTA", 1400, 3500),
    ("EWEDU", 1500, 3000),
    ("TOMATO STEW", 600, 2000),
    ("VEGETABLE SALAD", 1400, 4000),
    ("PASTA JOLLOF", 777, 3000),
    ("STEAMED VEGETABLE", 800, 2000),
    ("ENGLISH FRIED RICE", 1522.35, 5000),
    ("SNOW PASTA", 600, 3000),
    ("GREEN VEGETABLE SAUCE", 1041, 3000),
    ("CURRY FRIED RICE", 1426.05, 5000),
    ("VEGETABLE SOUP", 1179.35, 3000),
    ("BITTERLEAF", 1316.50, 3000),
    ("SNOW MACARONI", 600, 3000),
    ("PILAF RICE", 1410.65, 5000),
    ("VEGETABLE FRIED RICE", 2331.40, 5000),
    ("KUKA", 798.18, 2000),
    ("FRUIT PLATTER", 650, 2000),
    ("BEEF", 1300, 3500),
    ("NIGERIAN FRIED RICE", 859, 3000),
    ("FRESH FISH PEPPER SOUP", 2100, 5000),
    ("CORN AND CHICKEN SOUP", 1113, 3000),
    ("GOAT MEAT PEPPER SOUP", 1600, 5000),
    ("CHICKEN PEPPER SOUP", 1700, 5000),
    ("CHICKEN MINISTRONI", 1400, 3000),
    ("CREAM OF MUSHROOM SOUP", 1300, 3000),
    ("CREAM OF CHICKEN SOUP", 1200, 3000),
    ("GOLDEN YAM", 844, 3000),
    ("YAM PORRIDGE", 1500, 3000),
    ("MASHED POTATOES", 1000, 3000),
    ("FINGER FRIED YAM", 1000, 3000),
    ("HAND CUT FRIES", 1000, 3000),
    ("OVEN BAKED POTATOES", 1764, 3000),
    ("CHOCOLATE SLICED CAKE", 800, 1500),
    ("FRUIT CAKE", 900, 1500)
]
}

# -------------------------------- STREAMLIT SETUP -------------------------------- #
# Set page configuration
try:
    st.set_page_config(
        page_title="CRISPAN SUITE & EVENT CENTER JOS",
        layout="centered",
        page_icon="icon.ico"  # Ensure this file exists in the working directory
    )
except Exception as e:
    st.warning(f"Page icon could not be set. Error: {e}")

# -------------------------------- LOGIN FUNCTION -------------------------------- #
def login():
    st.title("CRISPAN SUITE & EVENT CENTER JOS")
    st.subheader("COST ANALYSIS APPLICATION")

    # Sidebar logo
    try:
        sidebar_img = Image.open("LOGO.png")  # Adjust the path to your logo
        sidebar_img = sidebar_img.resize((80, 80))
        st.sidebar.image(sidebar_img, use_container_width=True)
    except FileNotFoundError:
        st.sidebar.warning("Sidebar logo image not found. Please verify the file path.")

    # Login form
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state.logged_in = True
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid username or password")
            st.session_state.logged_in = False

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# -------------------------------- FUNCTIONS -------------------------------- #
def calculate_and_save(organization, selected_category, selected_meals, number_of_people):
    try:
        if not selected_category:
            raise ValueError("Please select a meal category.")
        if not selected_meals:
            raise ValueError("Please select at least one meal.")
        if number_of_people <= 0:
            raise ValueError("Number of people must be greater than zero.")

        selected_meal_names = []
        total_cost = 0
        total_selling_price = 0  # Initialize selling price

        # Calculate total cost and total selling price based on selected meals
        for meal_name, meal_cost, meal_selling_price in selected_meals:
            selected_meal_names.append(meal_name)
            total_cost += meal_cost * number_of_people
            total_selling_price += meal_selling_price * number_of_people  # Use selling price for the meal

        contribution_margin = total_selling_price - total_cost
        cost_margin = (total_cost / total_selling_price) * 100 if total_selling_price else 0

        current_date = datetime.now().strftime('%Y-%m-%d')
        day_of_week = datetime.now().strftime('%A')

        cursor.execute("""
        INSERT INTO orders (
            organization, meal_category, selected_meals, number_of_people, total_cost,
            total_selling_price, contribution_margin, cost_margin, date, day_of_week
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            organization, selected_category, ", ".join(selected_meal_names), number_of_people,
            total_cost, total_selling_price, contribution_margin, cost_margin,
            current_date, day_of_week
        ))
        conn.commit()
        st.success("Order saved successfully!")

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

def display_orders(start_date=None, end_date=None):
    query = "SELECT * FROM orders"
    if start_date and end_date:
        query += " WHERE date BETWEEN ? AND ?"
        cursor.execute(query, (start_date, end_date))
    else:
        cursor.execute(query)

    records = cursor.fetchall()
    if not records:
        st.write("No records found")
    else:
        df = pd.DataFrame(records, columns=["ID", "Organization", "Meal Category", "Selected Meals", "Number of People",
                                            "Total Cost", "Total Selling Price", "Contribution Margin", "Cost Margin",
                                            "Date", "Day of Week"])
        st.write(df)

def export_to_csv():
    cursor.execute("SELECT * FROM orders")
    records = cursor.fetchall()
    if not records:
        st.write("No records to export.")
    else:
        filename = f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Organization", "Meal Category", "Selected Meals", "Number of People",
                             "Total Cost", "Total Selling Price", "Contribution Margin", "Cost Margin", "Date", "Day of Week"])
            writer.writerows(records)
        st.success(f"Records exported successfully to {filename}")

# -------------------------------- STREAMLIT LAYOUT -------------------------------- #
st.sidebar.header("Navigation")
app_mode = st.sidebar.radio(
    "Select an option",
    ["🏠 Home", 
     "📋 View Orders", 
     "📂 Export Orders", 
     "💼 Menu Engineering", 
     "💵 Room and Hall Costing", 
     "🏊‍♂️ Recreation", 
     "🧺 Laundry"]
)

if app_mode == "🏠 Home":
    st.header("Enter Order Details")

    organization = st.text_input("Organization Name")
    meal_category = st.selectbox("Select Meal Category", options=MEAL_CATEGORIES.keys())
    selected_meals = st.multiselect("Select Meals", options=[meal[0] for meal in MEAL_CATEGORIES[meal_category]])
    number_of_people = st.number_input("Number of People", min_value=1)

    if st.button("Save Order"):
        selected_meal_info = [meal for meal in MEAL_CATEGORIES[meal_category] if meal[0] in selected_meals]
        calculate_and_save(organization, meal_category, selected_meal_info, number_of_people)

elif app_mode == "📋 View Orders":
    st.header("View All Orders")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date", min_value=start_date)

    if start_date and end_date:
        st.write(f"Displaying orders from **{start_date}** to **{end_date}**")
        display_orders(start_date=start_date, end_date=end_date)
    else:
        display_orders()

elif app_mode == "📂 Export Orders":
    st.header("Export Orders to CSV")
    export_to_csv()

elif app_mode == "💼 Menu Engineering":
    st.header("Menu Engineering")
    st.markdown("[Click here to view Menu Engineering Costing](https://menu-engineering.streamlit.app/)", unsafe_allow_html=True)

elif app_mode == "💵 Room and Hall Costing":
    st.header("Room and Hall Costing")
    st.markdown("[Click here to view Room and Hall Costing](https://room-hallcosting.streamlit.app/)", unsafe_allow_html=True)

elif app_mode == "🏊‍♂️ Recreation":
    st.header("Recreation Costing")
    recreation_option = st.radio(
        "Select Recreation Activity",
        ["💆‍♀️ Spa", "💪 Gym", "🏊‍♂️ Swimming Pool"]
    )
    if recreation_option == "💆‍♀️ Spa":
        st.markdown("[Click here to view Spa Costing](https://spa-costing.streamlit.app/)", unsafe_allow_html=True)
    elif recreation_option == "💪 Gym":
        st.markdown("[Click here to view Gym Costing](https://gym-costing.streamlit.app/)", unsafe_allow_html=True)
    elif recreation_option == "🏊‍♂️ Swimming Pool":
        st.markdown("[Click here to view Swimming Pool Costing](https://swimming-cost.streamlit.app/)", unsafe_allow_html=True)

elif app_mode == "🧺 Laundry":
    st.header("Laundry Costing")
    st.markdown("[Click here to view Laundry Costing](https://laundry-costing.streamlit.app/)", unsafe_allow_html=True)

# -------------------------------- FOOTER -------------------------------- #
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Contact: costcontroller@crispanhotel.com | Phone: +2348168950765", unsafe_allow_html=True)

# Close database connection
conn.close()