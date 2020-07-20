import pandas as pd
import numpy as np
from datetime import datetime

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import mlflow.sklearn
import mlflow.keras
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras import datasets, layers, models, utils
from tensorflow.keras.models import Sequential, load_model, save_model, Model
from tensorflow.keras.layers import Dense

app = Flask(__name__)

# Converts user age input into a one-hot-encoded array
def age_code(age_range):
    # Define age ranges and assign them to an index using a dictionary
    ages = {
        "1": 11,
        "1_4": 0,
        "5_14":5,
        "15_24":1,
        "25_34":2,
        "35_44":3,
        "45_54":4,
        "55_64":6,
        "65_74":7,
        "75_84":8,
        "85_over":9,
        "not_stated":10
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    age_array = [0 for x in range(len(ages))]

    # Change the value of the correct age to 1
    age_array[ages[age_range]] = 1

    return age_array

# Converts user gender input into a one-hot-encoded array
def gender_code(gender):
    # Define genders and assign them to an index using a dictionary
    genders = {
        "Male":1,
        "Female":0
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    gender_array = [0 for x in range(len(genders))]

    # Change the value of the correct gender to 1
    gender_array[genders[gender]] = 1

    return gender_array

# Converts user marital status input into a one-hot-encoded array
def marital_status_code(marital_status):
    # Define marital statuses and assign them to an index using a dictionary
    marital_statuses = {
        "Married":2,
        "Widowed":4,
        "Divorced":0,
        "Single":3,
        "Unknown":1
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    marital_status_array = [0 for x in range(len(marital_statuses))]

    # Change the value of the correct marital stauts to 1
    marital_status_array[marital_statuses[marital_status]] = 1

    return marital_status_array

# Converts user education level input into a one-hot-encoded array
def education_level_code(education_level):
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

# Gets current month and converts it into a one-hot-encoded array
def month_code():
    month_array = [0 for x in range(12)]
    month_recode = [4,3,7,0,8,6,5,1,11,10,9,2]
    current_month_index = datetime.today().month - 1
    month_array[month_recode[current_month_index]] = 1
    
    return month_array

def get_year():
    year = datetime.today().year
    return year

def get_age_plus_ten(age_range):
    # Define age ranges and assign them to a new age range using a dictionary
    ages = {
        "1": "5_14",
        "1_4": "5_14",
        "5_14": "15_24",
        "15_24":"25_34",
        "25_34":"35_44",
        "35_44":"35_44",
        "45_54":"45_54",
        "55_64":"65_74",
        "65_74":"75_84",
        "75_84":"85_over",
        "85_over":"85_over",
        "not_stated":"not_stated"
    }

    return ages[age_range]

def run_model(age, gender, marital_status, education_level, race, model_path, encoder_path):
    ml_model = tf.keras.models.load_model(f"Neural_Network_Trained_Models/saved_model/{model_path}")
    encoder = LabelEncoder()
    encoder.classes_ = np.load(f"Neural_Network_Trained_Models/saved_model/{encoder_path}", allow_pickle=True)

    input_list = [get_year()] + month_code() + age_code(age) + education_level_code(education_level)\
                + gender_code(gender) + marital_status_code(marital_status) + race_code(race)
    df = pd.DataFrame([input_list])
    predictions = ml_model.predict(df)
    predicted_class_num = ml_model.predict_classes(df)
    predicted_class_string = encoder.inverse_transform(predicted_class_num)
    if predicted_class_string == "Other":
        predicted_accuracy = 100 - predictions[0,1]*100
    else:
        predicted_accuracy = predictions[0,1]*100
    data = {"Class": predicted_class_string[0], "Probability": predicted_accuracy}
    return data

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

@app.route("/model/<age>/<gender>/<marital_status>/<education_level>/<race>")
def model(age, gender, marital_status, education_level, race):
    model_1 = run_model(age, gender, marital_status, education_level, race, "Model_1_External_Causes.h5", "model_1_classes.npy")
    model_2 = run_model(age, gender, marital_status, education_level, race, "Model_2_Cerebrovascular.h5", "model_2_classes.npy")
    model_3 = run_model(age, gender, marital_status, education_level, race, "Model_3_Alzheimers.h5", "model_3_classes.npy")
    model_4 = run_model(age, gender, marital_status, education_level, race, "Model_4_Diabetes.h5", "model_4_classes.npy")
    model_5 = run_model(age, gender, marital_status, education_level, race, "Model_5_Respiratory.h5", "model_5_classes.npy")
    return jsonify([model_1, model_2, model_3, model_4, model_5])

@app.route("/model_plus_10/<age>/<gender>/<marital_status>/<education_level>/<race>")
def model_plus_10(age, gender, marital_status, education_level, race):
    model_1 = run_model(get_age_plus_ten(age), gender, marital_status, education_level, race, "Model_1_External_Causes.h5", "model_1_classes.npy")
    model_2 = run_model(get_age_plus_ten(age), gender, marital_status, education_level, race, "Model_2_Cerebrovascular.h5", "model_2_classes.npy")
    model_3 = run_model(get_age_plus_ten(age), gender, marital_status, education_level, race, "Model_3_Alzheimers.h5", "model_3_classes.npy")
    model_4 = run_model(get_age_plus_ten(age), gender, marital_status, education_level, race, "Model_4_Diabetes.h5", "model_4_classes.npy")
    model_5 = run_model(get_age_plus_ten(age), gender, marital_status, education_level, race, "Model_5_Respiratory.h5", "model_5_classes.npy")
    return jsonify([model_1, model_2, model_3, model_4, model_5])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)
