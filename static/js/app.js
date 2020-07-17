async function buildPlot() {
    /* data route */
    const url = "/api/pals";

    const response = await d3.json(url);
    console.log(response);
    const data = [response];
    
    const layout = {
        title: "Pet Pals",
        xaxis: {
            title: "Pet Type"
        },
        yaxis: {
            title: "Number of Pals"
        }
    };
  
    Plotly.newPlot("plot", data, layout);
}

buildPlot();
