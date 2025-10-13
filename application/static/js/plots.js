console.log(testPlot.data);
console.log(testPlot.layout);
Plotly.newPlot("test-plot", testPlot.data, testPlot.layout, {responsive: true});