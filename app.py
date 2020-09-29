# Dependencies
import pandas as pd
import numpy as np
from datetime import datetime
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import xgboost as xgb

app = Flask(__name__)

# Converts user education level input into a one-hot-encoded array
def education_level_code(education_level):
    print(education_level)
    # Define education levels and assign them to an index using a dictionary
    education_levels = {
        "8th_grade":0,
        "9_12":1,
        "High_school":6,
        "Some_college":7,
        "Associate_degree":2,
        "Bachelors_degree":3,
        "Masters_degree":5,
        "Doctorate":4
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    education_level_array = [0 for x in range(len(education_levels))]

    # Change the value of the correct education level to 1
    education_level_array[education_levels[education_level]] = 1

    return education_level_array

# Gets current month and converts it into a one-hot-encoded array
def month_code():
    month_array = [0 for x in range(12)]
    month_recode = [4,3,7,0,8,6,5,1,11,10,9,2]
    current_month_index = datetime.today().month - 1
    month_array[month_recode[current_month_index]] = 1
    
    return month_array

# Converts user sex input into a one-hot-encoded array
def sex_code(sex):
    # Define sexes and assign them to an index using a dictionary
    sexes = {
        "Male":1,
        "Female":0
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    sex_array = [0 for x in range(len(sexes))]

    # Change the value of the correct sex to 1
    sex_array[sexes[sex]] = 1

    return sex_array

# Converts user age input into a one-hot-encoded array
def age_code(age_range):
    # Define age ranges and assign them to an index using a dictionary
    ages = {
        "1": 10,
        "1_4": 0,
        "5_14":5,
        "15_24":1,
        "25_34":2,
        "35_44":3,
        "45_54":4,
        "55_64":6,
        "65_74":7,
        "75_84":8,
        "85_over":9
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    age_array = [0 for x in range(len(ages))]

    # Change the value of the correct age to 1
    age_array[ages[age_range]] = 1

    return age_array

# Converts user marital status input into a one-hot-encoded array
def marital_status_code(marital_status):
    # Define marital statuses and assign them to an index using a dictionary
    marital_statuses = {
        "Married":1,
        "Widowed":3,
        "Divorced":0,
        "Single":2
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    marital_status_array = [0 for x in range(len(marital_statuses))]

    # Change the value of the correct marital stauts to 1
    marital_status_array[marital_statuses[marital_status]] = 1

    return marital_status_array

# Gets current day and converts it into a one-hot-encoded array
def day_code():
    day_array = [0 for x in range(7)]
    day_recode = [1,5,6,4,0,2,3]
    current_day_index = datetime.today().weekday()
    day_array[day_recode[current_day_index]] = 1
    
    return day_array

# Converts user race input into a one-hot-encoded array
def race_code(race):
    # Define races and assign them to an index using a dictionary
    races = {
        "White":3,
        "Black":2,
        "Asian":1,
        "American_Indian":0
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    race_array = [0 for x in range(len(races))]
    
    # Change the value of the correct race to 1
    race_array[races[race]] = 1

    return race_array

# Converts user race input into a one-hot-encoded array
def hispanic_code(hispanic):
    # Define hispanic_origins and assign them to an index using a dictionary
    hispanic_origins = {
        "Central or South American":0,
        "Cuban":1,
        "Mexican":2,
        "Non-Hispanic black":3,
        "Non-Hispanic other races":4,
        "Non-Hispanic white":5,
        "Other or unknown Hispanic":6,
        "Puerto Rican":7
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    hispanic_array = [0 for x in range(len(hispanic_origins))]
    
    # Change the value of the correct race to 1
    hispanic_array[hispanic_origins[hispanic]] = 1

    return hispanic_array

def sort_dict(dict):
    sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_dict

def format_prob(prob):
    probability = round(prob*100, 2)
    return str(probability)

def run_model(education_level, sex, age, marital_status, race, hispanic_origin, model_path):
    bst = xgb.XGBClassifier()
    bst.load_model(model_path)

    input_list = education_level_code(education_level) + month_code() + sex_code(sex) + age_code(age) \
                + marital_status_code(marital_status) + day_code() + race_code(race) + hispanic_code(hispanic_origin)
    df = pd.DataFrame([input_list])
    predictions = bst.predict(df.values)[0]
    print(predictions[2])
    prediction = {'Diseases of the circulatory system': format_prob(predictions[0]),
                  'Diseases of the nervous system': format_prob(predictions[1]),
                  'Neoplasms': format_prob(predictions[2])}
    prediction = sort_dict(prediction)
    print(prediction)
    return prediction

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def ml_app():
    return render_template("ml.html")

@app.route("/respiratory_diseases")
def respitory():
    return render_template("respiratory.html")

@app.route("/external_causes")
def external():
    return render_template("external.html")

@app.route("/nervous_system")
def nervous():
    return render_template("nervous.html")

@app.route("/metabolic_disorders")
def endocrine():
    return render_template("endocrine.html")

@app.route("/mental_disorders")
def mental():
    return render_template("mental.html")

@app.route("/model/<age>/<sex>/<marital_status>/<education_level>/<race>/<hispanic_origin>")
def model(age, sex, marital_status, education_level, race, hispanic_origin):
    model_predictions = run_model(education_level, sex, age, marital_status, race, hispanic_origin, 'Neural_Network_Trained_Models/global.model')
    return jsonify(model_predictions)
@app.route("/model_plus_10/<age>/<gender>/<marital_status>/<education_level>/<race>")
def model_plus_10(age, gender, marital_status, education_level, race):
    model_predictions = run_model(education_level, sex, get_age_plus_ten(age), marital_status, race, hispanic_origin, 'global.model')
    return jsonify(model_predictions)

# education = 'Bachelors_degree'
# sex = 'Male'
# age = '65_74'
# marital = 'Divorced'
# race = 'Black'
# hispanic = 'Cuban'
# model = 'global.model'
# predict = run_model(education, sex, age, marital, race, hispanic, model)

if __name__ == "__main__":
    app.run(debug=True)
