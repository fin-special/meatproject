
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 100, bottom: 30, left: 50},
        width = 960 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var container = d3.select("#pork")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("class","pk")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
    
    //Read the data
    
    d3.json("./static/pork_predict_price.json", function(data) {
      
        console.log(data)
        var parseDate = d3.timeParse("%Y-%m-%d");
    
        // 날짜형식 parser
        data.forEach(function(d) {
          d.ds = parseDate(d.ds);
        });

       
        // A color scale: one color for each group
        var myColor = d3.scaleOrdinal()
          .domain("yhat")
          .range(d3.schemeSet2);

        
        // Add X axis --> it is a date format
        var x = d3.scaleTime()
            .domain(d3.extent(data, function(d) {return d.ds;}))
            .range([0, width])
        svg = d3.selectAll("g.pk")
        svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));
        
        
        // Add Y axis
        var y = d3.scaleLinear()
          .domain( [d3.min(data.map(function(d){
                return d.yhat
            })), d3.max(data.map(function(d){
                return d.yhat
            }))])
          .range([ height, 0 ]);
        svg.append("g")
          .attr("class", "y axis")
          .call(d3.axisLeft(y));
    
        
        // Initialize line with group a
        var line =  svg
          .append('g')
          .append("path")
            .datum(data)
            .attr("d", d3.line()
              .curve(d3.curveNatural)
              .x(function(d) { return x(+d.ds) })
              .y(function(d) { return y(+d.yhat) })
            )
            .attr("stroke", function(d){ return myColor("yhat") })
            .attr("class","lines")
            .style("stroke-width", 3)
            .style("fill", "none")
          
        // A function that update the chart
        function update() {
    
        
          // Give these new data to update line
          line
              .datum(data)
              .transition()
              .duration(1000)
              
              .attr("class","linep")
              .attr("d", d3.line()
                .curve(d3.curveNatural)
                .x(function(d) { return x(+d.ds) })
                .y(function(d) { return y(+d.yhat) })
              )
              .attr("stroke", function(d){ return myColor("yhat") })
          var mousecon = d3.selectAll("g.pk")
          var mouseG = mousecon.append("g")
                    .attr("class", "mouse-over-effects");
      
          var linep = document.getElementsByClassName('linep');
        
              
          var mousePerLine = mouseG.selectAll('.mouse-per-line')
            .data(data)
            .enter()
            .append("g")
            .attr("class", "mouse-per-line");
              
          mousePerLine.append("circle")
          .attr("r", 7)
          .style("stroke", "#000"
          )
          .style("fill", "none")
          .style("stroke-width", "1px")
          .style("opacity", "0");
      
          mousePerLine.append("text")
            .attr("transform", "translate(10,3)");
      
          mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
            .attr('width', width) // can't catch mouse events on a g element
            .attr('height', height)
            .attr('fill', 'none')
            .attr('pointer-events', 'all')
            .on('mouseout', function() { // on mouse out hide line, circles and text
              d3.select(".mouse-line")
                .style("opacity", "0");
              d3.selectAll(".mouse-per-line circle")
                .style("opacity", "0");
              d3.selectAll(".mouse-per-line text")
                .style("opacity", "0");
            })
            .on('mouseover', function() { // on mouse in show line, circles and text
              d3.select(".mouse-line")
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
                      idx = bisect(d.yhat, xDate);
                  
                  var beginning = 0,
                      end = linep[i].getTotalLength(),
                      target = null;
              
                  while (true){
                    target = Math.floor((beginning + end) / 2);
                    pos = linep[i].getPointAtLength(target);
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
       
             var t = document.getElementById('target2');
             t.addEventListener('click', function(){
                 update()
             });
  
      })
    
       
            // run the updateChart function with this selected option
        
    
    