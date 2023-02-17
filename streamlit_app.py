import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Menu')
  
streamlit.text('🥣 Omega 3 & Blueberry oatmeal')
streamlit.text('🥗 Keal, spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  #Next line to do request fixed a fruit
  #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
  #Next line to do request dinamic a fruit
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # Take the jason version of the response and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


# New section Frutyvice to display API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  #fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  # streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    back_from_fuction = get_fruityvice_data(fruit_choice)
    # output it in the screen as a table
    streamlit.dataframe(back_from_fuction)
except URLError as e:
  streamlit.error()
      





# drop next line
#streamlit.text(fruityvice_response.json()) # Just writes the  data to the screen


streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
#my_data_row = my_cur.fetchone() # Load just firts row
my_data_rows = my_cur.fetchall() # Load all rows
#streamlit.text("The fruit load list contains:")
streamlit.header("The fruit load list contains:")
# show juus first row
# streamlit.dataframe(my_data_row) 
# show all rows
streamlit.dataframe(my_data_rows) 

streamlit.text("What fruit would you like to add?")
add_my_fruit = streamlit.text_input('What fruit would you like to add?','ggg')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
