function publish_result(data, model) {
    var prediction_time = '';
    if (model === "model") {
        prediction_time = 'today';
    }
    else {
        prediction_time = 'ten years from now';
    }
    output_html = `If you were to die ${prediction_time}, what are the chances you would die from the following diseases?:<br/>`;
    data.forEach(disease => {
        output_html = output_html + `<u>${disease[0]}</u>: ${disease[1]}% <br />`;
    });
    if (model === "model") {
        document.getElementById("current_health").innerHTML = output_html;
    }
    else {
        document.getElementById("health_plus_10").innerHTML = output_html;
    }
    
}

function api_call(model) {
    if (model === "model") {
        document.getElementById("current_health").innerHTML = "Calculating...";
    }
    else {
        document.getElementById("health_plus_10").innerHTML = "Calculating...";
    }
    var age_range = d3.select("#age_dropdown").property("value");
    var gender = d3.select("#sex_dropdown").property("value");
    var marital_status = d3.select("#marital_dropdown").property("value");
    var education_level = d3.select("#education_dropdown").property("value");
    var race = d3.select("#race_dropdown").property("value");
    var hispanic_origin = d3.select("#hispanic_dropdown").property("value");

    fetch(`/${model}/${age_range}/${gender}/${marital_status}/${education_level}/${race}/${hispanic_origin}`)
        .then(response => response.json())
        .then(data => publish_result(data, model));
}