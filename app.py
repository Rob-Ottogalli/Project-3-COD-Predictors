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
        "1": 0,
        "1_4": 1,
        "5_14":2,
        "15_24":3,
        "25_34":4,
        "35_44":5,
        "45_54":6,
        "55_64":7,
        "65_74":8,
        "75_84":9,
        "85_over":10
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
        "Male":0,
        "Female":1
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
        "Married":0,
        "Widowed":1,
        "Divorced":2,
        "Single":3
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
        "High_school":2,
        "Some_college":3,
        "Associate_degree":4,
        "Bachelors_degree":5,
        "Masters_degree":6,
        "Doctorate":7
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
        "White":0,
        "Black":1,
        "Asian":2,
        "American_Indian":3
    }

    # Create an array with the same length as the dictionary and fill it with 0's
    race_array = [0 for x in range(len(races))]
    
    # Change the value of the correct race to 1
    race_array[races[race]] = 1

    return race_array

# Gets current month and converts it into a one-hot-encoded array
def month_code():
    month_array = [0 for x in range(12)]
    month_array[datetime.today().month] = 1
    
    return month_array

def get_year():
    year = datetime.today().year
    return year

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
    predicted_accuracy = predictions[0,1]*100
    data = {"Class": predicted_class_string[0], "Accuracy": predicted_accuracy}
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

@app.route("/model_1/<age>/<gender>/<marital_status>/<education_level>/<race>")
def model_1(age, gender, marital_status, education_level, race):
    model_1 = run_model(age, gender, marital_status, education_level, race, "Model_1_External_Causes.h5", "model_1_classes.npy")
    model_2 = run_model(age, gender, marital_status, education_level, race, "Model_2_Cerebrovascular.h5", "model_2_classes.npy")
    model_3 = run_model(age, gender, marital_status, education_level, race, "Model_3_Alzheimers.h5", "model_3_classes.npy")
    model_4 = run_model(age, gender, marital_status, education_level, race, "Model_4_Diabetes.h5", "model_4_classes.npy")
    model_5 = run_model(age, gender, marital_status, education_level, race, "Model_5_Respiratory.h5", "model_5_classes.npy")
    return jsonify([model_1, model_2, model_3, model_4, model_5])


if __name__ == "__main__":
    app.run(debug=True)
