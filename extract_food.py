import requests
import openai
from dotenv import load_dotenv
from detect import detect_food


load_dotenv()

openai.api_key = "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"
api_key = "gt1BCwZRdKisVBhmCB0WcYKW6jy7T8dzPSwdJOJO"


def save_image(img_url):
    img_data = requests.get(img_url).content
    with open('resources/image.jpg', 'wb') as handler:
        handler.write(img_data)


def get_text_from_image(url):
    save_image(url)
    return detect_food()


def get_openai_response(text):
    hehe = "Give me just the name of the food (not the classification) from the description: " + text
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=hehe,
        temperature=0,
        max_tokens=100
    )
    return response.choices[0].text

def call_API(foodName, apiKey):
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apiKey}&query={foodName}'
    r = requests.get(url)
    if r.status_code == 200:
        print("nice 1")
    return r.json()

def extract_food_data(url):
    foodNames = get_text_from_image(url)
    foodName = get_openai_response(foodNames)
    nutrient_data = dict()
    ans = call_API(foodName, api_key)
    if not ans:
        print("no such food exists")
        return None
    food = ans['foods'][0]

    for nutrient in food['foodNutrients']:
        nutrient_data[nutrient['nutrientName']] = nutrient['value']
    return give_output(food['description'], nutrient_data)

def give_output(name, nutritional_datas):
    nutrient_values = ""
    for nut, amount in nutritional_datas.items():
        nutrient_values += str(nut) + ": " + str(amount)
    food_prompt = "Give me a short description of " + name + " and all it's nutritional values which is listed as follows: " + nutritional_datas + "\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=food_prompt,
        temperature=0,
        max_tokens=100
    )
    return response.choices[0].text