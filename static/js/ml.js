// Converts user age input into a one-hot-encoded array
function age_code(age_range) {
    // Define age ranges and assign them to an index using a dictionary
    const ages = {
        "Under 1 year": 0,
        "1-4 years": 1,
        "5-14":2,
        "15-24":3,
        "25-34":4,
        "35-44":5,
        "45-54":6,
        "55-64":7,
        "65-74":8,
        "75-84":9,
        "85 years and over":10
    };

    // Create an array with the same length as the dictionary and fill it with 0's
    var age_array = [];
    for(var i = 0; i < Object.keys(ages).length; i++){ age_array.push(0);}

    // Change the value of the correct age to 1
    age_array[ages[age_range]] = 1;

    return age_array;
}

// Converts user gender input into a one-hot-encoded array
function gender_code(gender) {
    //Define genders and assign them to an index using a dictionary
    const genders = {
        "Male":0,
        "Female":1
    };

    // Create an array with the same length as the dictionary and fill it with 0's
    var gender_array = [];
    for(var i = 0; i < Object.keys(genders).length; i++){ gender_array.push(0);}

    // Change the value of the correct gender to 1
    gender_array[genders[gender]] = 1;

    return gender_array;
}

// Converts user marital status input into a one-hot-encoded array
function marital_status_code(marital_status) {
    //Define marital statuses and assign them to an index using a dictionary
    const marital_statuses = {
        "Married":0,
        "Widowed":1,
        "Divorced":2,
        "Never married, single":3
    };

    // Create an array with the same length as the dictionary and fill it with 0's
    var marital_status_array = [];
    for(var i = 0; i < Object.keys(marital_statuses).length; i++){ marital_status_array.push(0);}

    // Change the value of the correct marital stauts to 1
    marital_status_array[marital_statuses[marital_status]] = 1;

    return marital_status_array;
}

// Converts user education level input into a one-hot-encoded array
function education_level_code(education_level) {
    //Define education levels and assign them to an index using a dictionary
    const education_levels = {
        "8th grade or less":0,
        "9 - 12th grade, no diploma":1,
        "High school graduate or GED completed":2,
        "Some college credit, but no degree":3,
        "Associate degree":4,
        "Bachelor's degree":5,
        "Master's degree":6,
        "Doctorate or professional degree":7
    };

    // Create an array with the same length as the dictionary and fill it with 0's
    var education_level_array = [];
    for(var i = 0; i < Object.keys(education_levels).length; i++){ education_level_array.push(0);}

    // Change the value of the correct education level to 1
    education_level_array[education_levels[education_level]] = 1;

    return education_level_array;
}

// Converts user race input into a one-hot-encoded array
function race_code(race) {
    // Define races and assign them to an index using a dictionary
    const races = {
        "White":0,
        "Black":1,
        "Asian or Pacific Islander":2,
        "American Indian":3
    };

    // Create an array with the same length as the dictionary and fill it with 0's
    var race_array = [];
    for(var i = 0; i < Object.keys(races).length; i++){ race_array.push(0);}

    // Change the value of the correct race to 1
    race_array[races[race]] = 1;

    return race_array;
}

var ml_button = d3.select("#ml_button");

function ml_enter() {
    
}

ml_button.on("click", ml_enter);