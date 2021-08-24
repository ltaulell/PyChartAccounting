/**
 * Copyright (c) 2021
 *
 * long description for the file
 *
 * @summary file which contains the functions allowing the creation of charts
 * @author Damien LE BORGNE
 *
 * Created at     : 2021-03-07
 * Last modified  : 2021-03-11
 */


function generateLabelsData(labelsName, dataList){

}

listBackGroundColor = [
    "#f43004",
    "#decf3f",
    "#FFA500",
    "#9b59b6",
  ]

toolTips = {
    callbacks: {
        label: function(tooltipItem, data) {
        var dataset = data.datasets[tooltipItem.datasetIndex];
        var total = dataset.data.reduce(function(previousValue, currentValue, currentIndex, array) {
        return previousValue + currentValue;
    });
        var currentValue = dataset.data[tooltipItem.index];
        var percentage = Math.floor(((currentValue/total) * 100));         
        return currentValue +" ≃ "+ percentage + "%";
            }
        }
}

var legends = {
    display: true,
    position: 'right',
    labels: {
        generateLabels: function(chart) {
            var data = this.chart.data;
            if (data.labels.length && data.datasets.length) {
                return data.labels.map(function(label, i) {
                    var meta = chart.getDatasetMeta(0);
                    var datasets = data.datasets[0];
                    var arc = meta.data[i];
                    var custom = arc && arc.custom || {};
                    var getValueAtIndexOrDefault = Chart.helpers.getValueAtIndexOrDefault;
                    var arcOpts = chart.options.elements.arc;
                    var fill = custom.backgroundColor ? custom.backgroundColor : getValueAtIndexOrDefault(datasets.backgroundColor, i, arcOpts.backgroundColor);
                    var stroke = custom.borderColor ? custom.borderColor : getValueAtIndexOrDefault(datasets.borderColor, i, arcOpts.borderColor);
                    var bw = custom.borderWidth ? custom.borderWidth : getValueAtIndexOrDefault(datasets.borderWidth, i, arcOpts.borderWidth);

                    var value = chart.config.data.datasets[arc._datasetIndex].data[arc._index];

                    return {
                        text: label + " : ~" + Math.round(value*1000)/1000,
                        fillStyle: fill,
                        strokeStyle: stroke,
                        lineWidth: bw,
                        index: i
                    };
                });
            } else {
                return [];
            }
        }
    },
    onClick: null
}


function PieChart(IdChart, labelsName, dataList){

    var brandPrimary = 'rgba(179, 50, 155, 1)';

    var PieChartId    = $('#'+IdChart);

    var pieChart = new Chart.Doughnut(PieChartId, {
        data: {
            labels: labelsName,
            datasets: [
                {
                    data: dataList,
                    backgroundColor: [
                        brandPrimary,
                        "rgba(75,192,192,1)",
                        "#56ffce",
                        "rgba(250, 15, 15, 1)"
                    ],
                }]
            },
        options: {
            responsive: true,
            tooltips: toolTips,
            legend: legends
        }
    });

}

function BarChart(IdChart, labels, values){

    var BarChartId  = $('#'+IdChart);

    var barChart = new Chart.Bar(BarChartId, {
        data: {
            labels: labels,
            datasets: [
                {
                    backgroundColor: listBackGroundColor,
                    borderWidth: 1,
                    data: values,
                },
            ]
        }, 
        options: {
            responsive: true,
            tooltips: toolTips,
            legend: legends
        }
    });

}


/*
function BarChartStacked(IdChart, labels, values){

    var UserPrimary = 'rgba(51, 179, 90, 1)';
    var AllPrimary = 'rgba(203, 203, 203, 1)';
    var BarChartId  = $('#'+IdChart);

    var t = [];
    for (let i = 0; i < labels.length; i++) {
        var sayings = {
            label: labels[i],
            data: [values[i]],
            backgroundColor: listBackGroundColor[i],
            borderWidth: 1,
        };
        t.push(sayings);
    }
    console.log(t);

    var barChart = new Chart.Bar(BarChartId, {
        data: {
            labels: labels,
            datasets: t
        },
        options : {
            responsive: true,
            tooltips: toolTips,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        min: 0
                    },
                    stacked: true
                }], 
                xAxes: [{ stacked: true }]
            },

            
            
            legend: legends
        
        }
        
    });

}
*/