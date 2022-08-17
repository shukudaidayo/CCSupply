// This script populates the HTML table with data from Card_Supply.csv,
// populates the "Last Updated" paragraph with the Last Modified timestamp 
// of Card_Supply.csv, and creates a stacked column chart illustrating the
// card supply data
$(document).ready(() => {

  // Accordion mechanic
  const acc = document.getElementsByClassName("accordion");
  for (let i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
      this.classList.toggle("active");
      let panel = this.nextElementSibling;
      if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
      } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
      };
    });
  };

  // Get Last Modified timestamp of Card_Supply.csv
  try {
    const req = new XMLHttpRequest();
    req.open("HEAD", "data/Card_Supply.csv", false);
    req.send(null);
    if(req.status == 200){
      // Print Last Modified timestamp
      $('#lastModified').append(req.getResponseHeader("Last-Modified"));
    } else {
      // Print request error code
      $('#lastModified').append("ERROR: " + req.status);
    };
  } catch(err) {
    // Print function error code
    $('#lastModified').append("ERROR:" + err);
  };

  // Get supply data from Card_Supply.csv (output of CCSupply.py)
  const promise = $.ajax({
    type:"GET",
    dataType:"text",
    url:"data/Card_Supply.csv",
    cache:false
  });

  // Runs in case of success
  promise.done(data => {
    // Bool used to skip printing header row
    let headerRow = true;
    // Split csv file by rows
    const rowsArr = data.split("\n");
    // Iterate over rows
    $.each(rowsArr, function() {
      // Skip header row
      if (headerRow) {
        headerRow = false;
      } else {
        if (this != "") {
          // Split row by values
          let valArr = this.split(",");
          let row = "<tr>";
          let priority
          // Iterate over values
          $.each(valArr, function(valIndex) {
            // Assign class for responsive column hiding
            switch (valIndex) {
              case 0:
              case 2:
              case 6:
                priority = 1;
                break;
              case 1:
                priority = 2;
                break;
              case 3:
              case 4:
              case 5:
                priority = 3;
                break;
              default:
                console.log('Error in priority class assignment');
            };
            row += '<td class="priority-' + priority + '">' + this + "</td>";
          });
          row += "</tr>";
          // Add row to table
          $('tbody').append(row);
        }
      };
    });

    // Load Google Charts
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    // Callback that creates and populates data table,
    // instantiates the chart, passes in the data and
    // draws it
    function drawChart() {

      // Create the data table.
      const chartdata = new google.visualization.DataTable();
      chartdata.addColumn('string', "Card #");
      chartdata.addColumn('number', "Burned");
      chartdata.addColumn('number', "Inactive");
      chartdata.addColumn('number', "Active");

      // Populate table with data from Card_Supply.csv
      headerRow = true;
      let indexArr = [];
      $.each(rowsArr, function() {
        let newRow = [];
        if (headerRow) {
          // Use header row to find indices of burned/inactive/active supply columns
          let valArr = this.split(",");
          $.each(valArr, function(headerIndex) {
            if (valArr[headerIndex] === "Total Burned Cards" 
              || valArr[headerIndex] === "Inactive Wallet Supply" 
              || valArr[headerIndex] === "Active Supply") {
              indexArr.push(headerIndex);
            };
          });
          headerRow = false;
        } else {
          // Add card # and supply data to chartdata table
          if (this != "") {
            newRow = [];
            let valArr = this.split(",");
            $.each(valArr, function(valIndex) {
              if (valIndex === 0) {
                newRow.push(valArr[valIndex]);
              } else if (valIndex === indexArr[0] 
                || valIndex === indexArr[1] 
                || valIndex === indexArr[2]) {
                newRow.push(Number(valArr[valIndex]));
              };
            });
            chartdata.addRow(newRow);
          };
        };
      });

      // Set chart options
      const options = {
                      isStacked: true,
                      colors: ['red', 'gold', 'green'],
                      hAxis: {
                        title: 'Card Number',
                        textStyle: {fontName: 'Montserrat', fontSize: '16'},
                        titleTextStyle: {fontName: 'Montserrat', fontSize: '18'}
                      },
                      vAxis: {
                        title: 'Card Supply',
                        textStyle: {fontName: 'Montserrat', fontSize: '16'},
                        titleTextStyle: {fontName: 'Montserrat', fontSize: '18'}
                      },
                      legend: {
                        position: 'top',
                        alignment: 'center',
                        textStyle: {fontName: 'Montserrat', fontSize: '18'}
                      },
                      chartArea: {
                        width: '75%',
                        height: '65%'
                      },
                      tooltip: {
                        textStyle: {fontName: 'Montserrat'}
                      }
                      };

      // Instantiate and draw chart, passing in options
      const chart = new google.visualization.ColumnChart(document.getElementById('chart-div'));
      // Make html visible only once chart is ready
      google.visualization.events.addListener(chart, 'ready', function () {
        document.getElementsByTagName("html")[0].style.visibility = "visible";
      });
      chart.draw(chartdata, options);
    };

    // Make chart responsive
    $(window).resize(function() {
      drawChart();
    });
  });

  // Runs in case of failure
  promise.fail(function() {
    console.log('Failed to read Card_Supply.csv');
  });
});
