function get_disease(index) {
    const diseases = ["External Causes","Cerebrovascular diseases","Mental disorders",
                    "Metabolic diseases","Respiratory diseases"]
    return diseases[index];
}

function get_disease_path(index) {
    const paths = ["/external_causes","/nervous_system","/mental_disorders","/metabolic_disorders",
                    "respiratory_diseases"];
    return paths[index];
}

function get_result_index(data) {
    var final_disease_index = 0;
    var highest_probability = 0;
    data.forEach((disease, index) => {
        if (disease["Probability"] > highest_probability) {
            highest_probability = disease["Probability"];
            final_disease_index = index;
        }
    });
    return final_disease_index
}

function publish_result(data) {
    index = get_result_index(data);
    disease = get_disease(index);
    disease_path = get_disease_path(index);
    document.getElementById("demo").innerHTML = `You are most likely to die of ${disease}. 
                                                Find out more <a href=${disease_path}  >here</a>`;
}

function api_call() {
    document.getElementById("demo").innerHTML = "Calculating...";
    var age_range = d3.select("#age_dropdown").property("value");
    var gender = d3.select("#gender_dropdown").property("value");
    var marital_status = d3.select("#marital_dropdown").property("value");
    var education_level = d3.select("#education_dropdown").property("value");
    var race = d3.select("#race_dropdown").property("value");

    fetch(`/model/${age_range}/${gender}/${marital_status}/${education_level}/${race}`)
        .then(response => response.json())
        .then(data => publish_result(data));
}