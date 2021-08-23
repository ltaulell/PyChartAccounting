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
    onClick:function(e, legendItem){
        var index = legendItem.index;
        var ci = this.chart;
        var meta = ci.getDatasetMeta(0);
        var CurrentalreadyHidden = (meta.data[index].hidden==null) ? false : (meta.data[index].hidden);
        var allShown=true;
        $.each(meta.data,function(ind0,val0){
            if(meta.data[ind0].hidden){
                allShown=false;
                return false; 
            }else{
                allShown=true;
            }
        });
        if(allShown){
            $.each(meta.data,function(ind,val){
                if(meta.data[ind]._index===index){
                    meta.data[ind].hidden=false;
                }else{
                    meta.data[ind].hidden=true;
                }
            });
        }else{
            if(CurrentalreadyHidden){
                $.each(meta.data,function(ind,val){
                    if(meta.data[ind]._index===index){
                        meta.data[ind].hidden=false;
                    }else{
                        meta.data[ind].hidden=true;
                    }
                });
            }else{
                $.each(meta.data,function(ind,val){
                    meta.data[ind].hidden=false;
                }); 
             }
         }
        ci.update();

    }
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
            tooltips: {
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
                },
                title: {
                    display: true,
                    text: 'Custom Chart Title'
                }
            },
            legend: legends
        }
    });

}



function LineChart(IdChart){

    var linePrimary = 'rgba(51, 179, 90, 1)';
    var LineChartId  = $('#'+IdChart);

    var lineChart = new Chart.Line(LineChartId, {
        data: {
          labels: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
          datasets: [{
            label: "Utilisateur",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(51, 179, 90, 0.38)",
                    borderColor: linePrimary,
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    borderWidth: 1,
                    pointBorderColor: linePrimary,
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: linePrimary,
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [10, 20, 30, 40, 50, 60, 60, 50, 40, 30, 20, 10],
                    spanGaps: false
          }]
        },
        options: {
          responsive: true,
          tooltips: {
            mode: 'index',
            intersect: true
          }
        }
      });
}

function BarChart(IdChart, labels, values){

    const chartLegendSelector = "[data-results-chart-legends]";
    let chartLegendEL = document.querySelector(chartLegendSelector);

    var UserPrimary = 'rgba(51, 179, 90, 1)';
    var AllPrimary = 'rgba(203, 203, 203, 1)';
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
                },
            responsive: true,
            legend: legends
        }
    });

}



function BarChartStacked(IdChart, labels, values){

    var UserPrimary = 'rgba(51, 179, 90, 1)';
    var AllPrimary = 'rgba(203, 203, 203, 1)';
    var BarChartId  = $('#'+IdChart);

    var barChart = new Chart.Bar(BarChartId, {
        data: {
            datasets: [
                {
                    label: pgLabel,
                    backgroundColor: UserPrimary,
                    borderColor: UserPrimary,

                    borderWidth: 1,
                    data: [pgValue],
                },
                {
                    label: ppLabel,
                    backgroundColor: AllPrimary,

                    borderColor: AllPrimary,

                    borderWidth: 1,
                    data: [ppValue],
                }
            ]
        },
        options : {
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

        }
    });

}


function BarChartCompare(IdChart, labels, values){
    if(values[0] < values[1]){
        pgValue = values[1];
        ppValue = values[0];
        pgLabel = labels[1];
        ppLabel = labels[0];
    }
    var UserPrimary = 'rgba(51, 179, 90, 1)';
    var AllPrimary = 'rgba(203, 203, 203, 1)';
    var BarChartId  = $('#'+IdChart);

    var barChart = new Chart.Bar(BarChartId, {
        data: {
            datasets: [
                {
                    label: pgLabel,
                    backgroundColor: UserPrimary,
                    borderColor: UserPrimary,

                    borderWidth: 1,
                    data: [pgValue],
                },
                {
                    label: ppLabel,
                    backgroundColor: AllPrimary,

                    borderColor: AllPrimary,

                    borderWidth: 1,
                    data: [ppValue],
                }
            ]
        },
        options : {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        min: 0
                    }
                }]
            },

        }
    });

}
