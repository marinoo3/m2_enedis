const contentElement = document.querySelector('.content');
contentElement.classList.remove('loading');


Plotly.newPlot("scatter-plot", scatterPlot.data, scatterPlot.layout, {responsive: true});
Plotly.newPlot("box-plot", boxPlot.data, boxPlot.layout, {responsive: true});
Plotly.newPlot("bar-plot", barPlot.data, barPlot.layout, {responsive: true});
Plotly.newPlot("bar-dpe-plot", barDPEPlot.data, barDPEPlot.layout, {responsive: true});
Plotly.newPlot("heatmap-plot", heatmapPlot.data, heatmapPlot.layout, {responsive: true});


