var request = new XMLHttpRequest()
var myData = [];


request.open('GET', 'https://wwtu45hna4.execute-api.us-west-2.amazonaws.com/prod', true)

request.onload = function() {
    
    // Begin accessing JSON data here
    var data = JSON.parse(this.response)
    console.log(data)
    data.forEach(function (date) {
        myData.push([date.date, date.cases, date.deaths, date.recoveries]);
    });

    sortedData = myData.sort()

    google.charts.load('current', {
        'packages': ['line', 'table']
    });

    google.charts.setOnLoadCallback(drawChart);
    google.charts.setOnLoadCallback(drawTable);
    google.charts.setOnLoadCallback(drawTable2);
    google.charts.setOnLoadCallback(drawTable3);


    //Line chart
    function drawChart() {

        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Date');
        data.addColumn('number', 'Total Cases');
        data.addColumn('number', 'Total Deaths');
        data.addColumn('number', 'Total Recovered');

        data.addRows(sortedData);

        var options = {
            chart: {
            },

        };

        var chart = new google.charts.Line(document.getElementById('linechart_material'));

        chart.draw(data, google.charts.Line.convertOptions(options));
    }


    //Full table with all data
    function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Date');
        data.addColumn('number', 'Total Cases');
        data.addColumn('number', 'Total Deaths');
        data.addColumn('number', 'Total Recovered');

        data.addRows(sortedData);
        var options = {

            allowHtml: true,
            sortAscending: false,
            sortColumn: 0,
        };

        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, options);
    }

    var curCases = sortedData[sortedData.length - 1][1]
    var prevCases = sortedData[sortedData.length - 2][1]
    var cngCases = curCases - prevCases

    //DailyCases past 24 hours chart
    function drawTable2() {
        var data = new google.visualization.DataTable();
        data.addColumn('number', 'Daily Cases (Past 24 hours)');


        data.addRows([
            [cngCases]
        ]);
        var options = {
            allowHtml: true,
        };

        var table = new google.visualization.Table(document.getElementById('table_div2'));

        table.draw(data, options);
    }

    var curDeaths = sortedData[sortedData.length - 1][2]
    var prevDeaths = sortedData[sortedData.length - 2][2]
    var cngDeaths = curDeaths - prevDeaths

    //Daily Deaths past 24 hours chart
    function drawTable3() {
        var data = new google.visualization.DataTable();
        data.addColumn('number', 'Daily Deaths (Past 24 hours)');


        data.addRows([
            [cngDeaths]
        ]);
        var options = {
            allowHtml: true,

        };

        var table = new google.visualization.Table(document.getElementById('table_div3'));

        table.draw(data, options);
    }


    window.addEventListener('resize', drawChart, false);
    window.addEventListener('resize', drawTable, false);
    window.addEventListener('resize', drawTable2, false);
    window.addEventListener('resize', drawTable3, false);

}

request.send()