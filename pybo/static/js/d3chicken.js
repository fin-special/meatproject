
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 100, bottom: 30, left: 50},      
        width = 960 - margin.left - margin.right,
        height = 700 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#chicken")
      .append("svg")
        // .attr("width", width + margin.left + margin.right)
        // .attr("height", height + margin.top + margin.bottom)
      .attr("viewBox", '0 0 900 400')
      .append("g")
        .attr("class","ch") /* (수정) 1단계 - 요소영향 X */
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
    
    //Read the data
    
    d3.json("./static/json/chicken_predict_price.json", function(data) {

      
          
        var parseDate = d3.timeParse("%Y-%m-%d");
    
        // 날짜형식 parser
        data.forEach(function(d) {
          d.ds = parseDate(d.ds);
        });

        // List of groups (here I have one group per column)
        var allGroup = ["p5_6","p7_8","p9_10","p11","p12","p13_16"]
        // add the options to the buttons
        d3.select("#selectButton")
          .selectAll('myOptions')
          .data(allGroup)
          .enter()
            .append('option')
          .text(function (d) {
                if(d=="p5_6") d="5-6호";
                else if(d=="p7_8") d="7-8호"
                else if(d=="p9_10") d="9-10호"
                else if(d=="p11")  d="11호"
                else if(d=="p12") d="12호"
                else if(d=="p13_16") d="13-16호"
                return d
             }) // text showed in the menu
          .attr("value", function (d) { return d; }) // corresponding value returned by the button
    
        // A color scale: one color for each group
        var myColor = d3.scaleOrdinal()
          .domain(allGroup)
          .range(d3.schemeSet2);

        // Add X axis --> it is a date format
        var x = d3.scaleTime()
            .domain(d3.extent(data, function(d) {return d.ds;}))
            .range([0, width])
        svg = d3.selectAll("g.ch")  
        svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));
        
        
        // Add Y axis
        var y = d3.scaleLinear()
          .domain( [d3.min(data.map(function(d){
                return d.p5_6
            })), d3.max(data.map(function(d){
                return d.p5_6
            }))])
          .range([ height, 0 ]);
        var yAxis = svg.append("g")
          .attr("class", "y")
          .call(d3.axisLeft(y));
    
        
        // Initialize line with group a
        var line = svg
          .append('g')
          .append("path")
            .datum(data)
            .attr("d", d3.line()
              .curve(d3.curveNatural)
              .x(function(d) { return x(+d.ds) })
              .y(function(d) { return y(+d.p5_6) })
            )
            .attr("stroke", function(d){ return myColor("p5_6") })
            .attr("class","line")
            .style("stroke-width", 3)
            .style("fill", "none")

          
        
  
        // A function that update the chart
        function update(selectedGroup) {
    
          // Create new data with the selection?
          var dataFilter = data.map(function(d){return {ds: d.ds, price:d[selectedGroup]} })


          
       
      
          
          console.log(dataFilter)
          //update Y axis
          y.domain( [d3.min(dataFilter.map(function(d){
                  return d.price
              })), d3.max(dataFilter.map(function(d){
                  return d.price
              }))])

          yAxis
              .transition()
              .duration(1000)
              .call(d3.axisLeft(y));
          
            
          

          
          // Give these new data to update line
          line
              .datum(dataFilter)
              .transition()

              .duration(2000)
              .attr("class","line")
              .attr("d", d3.line()
                .curve(d3.curveNatural)

                .x(function(d) { return x(+d.ds) })
                .y(function(d) { return y(+d.price) })
              )
              .attr("stroke", function(d){ return myColor(selectedGroup) })
          

          var mousecon = d3.selectAll("g.ch")
          var mouseG = mousecon.append("g")
          // var mouseG = svg.append("g")

                    .attr("class", "mouse-over-effects");
      
          var lines = document.getElementsByClassName('line');
        
              
          var mousePerLine = mouseG.selectAll('.mouse-per-line')
            .data(dataFilter)
            .enter()
            .append("g")
            .attr("class", "mouse-per-line");
              
          mousePerLine.append("circle")
          .attr("r", 7)
          .style("stroke", "#000")
          .style("fill", "none")
          .style("stroke-width", "1px")
          .style("opacity", "0");
      
          mousePerLine.append("text")
            .attr("transform", "translate(10,3)");
      
          mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas

            .attr('width',width) // can't catch mouse events on a g element

            .attr('height', height)
            .attr('fill', 'none')
            .attr('pointer-events', 'all')
            .on('mouseout', function() { // on mouse out hide line, circles and text
              d3.select(".mouse-line1")
                .style("opacity", "0");
              d3.selectAll(".mouse-per-line circle")
                .style("opacity", "0");
              d3.selectAll(".mouse-per-line text1")
                .style("opacity", "0");
            })
            .on('mouseover', function() { // on mouse in show line, circles and text
              d3.select(".mouse-line1")
                .style("opacity", "1");
              d3.selectAll(".mouse-per-line circle")
                .style("opacity", "1");
              d3.selectAll(".mouse-per-line text")
                .style("opacity", "1");
            })
            .on('mousemove', function() { // mouse moving over canvas
              var mouse = d3.mouse(this);
              d3.select(".mouse-line")
                .attr("d", function() {
                  var d = "M" + mouse[0] + "," + height;
                  d += " " + mouse[0] + "," + 0;
                  return d;
                });
              
              d3.selectAll(".mouse-per-line")
                .attr("transform", function(d, i) {
                  var xDate = x.invert(mouse[0]),
                      bisect = d3.bisector(function(d) { return d.ds; }).right;
                      
                      idx = bisect(d.price, xDate);
                  
                  var beginning = 0,
                      end = lines[i].getTotalLength(),
                      target = null;
              
                  while (true){
                    target = Math.floor((beginning + end) / 2);
                    pos = lines[i].getPointAtLength(target);
                    if ((target === end || target === beginning) && pos.x !== mouse[0]) {
                        break;
                    }
                    if (pos.x > mouse[0])      end = target;
                    else if (pos.x < mouse[0]) beginning = target;
                    else break; //position found
                  }
                  
                  d3.select(this).select('text')
                    .text(y.invert(pos.y).toFixed(2));
                    
                  
                  return "translate(" + mouse[0] + "," + pos.y +")";
                });
            });
            
        }
    
        // When the button is changed, run the updateChart function
        d3.select("#selectButton").on("change", function(d) {
            // recover the option that has been chosen
            var selectedOption = d3.select(this).property("value")
            // run the updateChart function with this selected option
            update(selectedOption)
        })
    })
    