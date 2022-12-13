
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
    
    // append the div for tooltip object
    var chicken_tooltip = d3.select("#chicken").append("div")
    .attr("class", "tooltip")
    .style("display", "none");
    //Read the data
    
    d3.json("./static/json/chicken_predict_price.json", function(data) {

      
          
      var parseDate = d3.timeParse("%Y-%m-%d");
      bisectDate = d3.bisector(function(d) { return d.ds; }).left,
      formatValue = d3.format(",")
      dateFormatter = d3.timeFormat("%m/%d/%y");

    
        // 데이터정제 (날짜 parsing 가격 소수점제거)
        data.forEach(function(d) {
          d.ds = parseDate(d.ds);
          d.p5_6  =  parseInt(d.p5_6)
          d.p7_8  =  parseInt(d.p7_8)
          d.p9_10 =  parseInt(d.p9_10)
          d.p11   =  parseInt(d.p11)
          d.p12   =  parseInt(d.p12)
          d.p13_16 = parseInt(d.p13_16)
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
            .domain([data[0].ds, data[data.length - 1].ds])
            .range([0, width])
        svg = d3.selectAll("g.ch")  
        svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x)
                  .tickFormat(dateFormatter));
        
        
        // Add Y axis
        var y = d3.scaleLinear()
          .domain( [d3.min(data.map(function(d){
                return d.p5_6 - 100
            })), d3.max(data.map(function(d){
                return d.p5_6 + 100
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

          
         // append hovering mousecursor circle
         var focus = svg.append("g")
         .attr("class", "focus")
         .style("display", "none");

         focus.append("circle")
             .attr("r", 5);
    
            // tooltip-date
          chicken_tooltip.append("div")
             .attr("class", "tooltip-date");
 
         var tooltipLikes = chicken_tooltip.append("div");
         tooltipLikes.append("span")
             .attr("class", "tooltip-title")
             .text("Price: ");
            // tooltip-likes
          tooltipLikes.append("span")
             .attr("class", "tooltip-likes");
  
             svg.append("rect")
             .attr("class", "overlay")
             .attr("width", width)
             .attr("height", height)
             .on("mouseover", function() { focus.style("display", null); })
             .on("mouseout", function() { focus.style("display", "none"); })
             .on("mousemove", mousemove);
          
             function mousemove() {
                 var x0 = x.invert(d3.mouse(this)[0]),
                     i = bisectDate(data, x0, 1),
                     d0 = data[i - 1],
                     d1 = data[i],
                     d = x0 - d0.ds > d1.ds - x0 ? d1 : d0;
                 focus.attr("transform", "translate(" + x(d.ds) + "," + y(d.p5_6) + ")");
                 chicken_tooltip.attr("style", "left:" + (x(d.ds) +700) + "px;top:"+ (y(d.p5_6)+300) + "px;"  );    // 툴팁위치 
                 chicken_tooltip.select(".tooltip-date").text(dateFormatter(d.ds));
                 chicken_tooltip.select(".tooltip-likes").text(formatValue(d.p5_6));
             }
        
        // A function that update the chart
        function update(selectedGroup) {
    
          d3.selectAll("rect.overlay").remove()
          // Create new data with the selection?
          var dataFilter = data.map(function(d){return {ds: d.ds, price:d[selectedGroup]} })

          //update Y axis
          y.domain( [d3.min(dataFilter.map(function(d){
                  return d.price - 200
              })), d3.max(dataFilter.map(function(d){
                  return d.price + 100
              }))])

          yAxis
              .transition()
              .duration(1000)
              .call(d3.axisLeft(y));
          
            
          

          
          // Give these new data to update line
          line
              .datum(dataFilter)
              .transition()

              .duration(1000)
              .attr("class","line")
              .attr("d", d3.line()
                .curve(d3.curveNatural)

                .x(function(d) { return x(+d.ds) })
                .y(function(d) { return y(+d.price) })
              )
              .attr("stroke", function(d){ return myColor(selectedGroup) })

              svg = d3.selectAll("g.ch")  
              svg.append("rect")
              .attr("class", "overlay")
              .attr("width", width)
              .attr("height", height)
              .on("mouseover", function() { focus.style("display", null); })
              .on("mouseout", function() { focus.style("display", "none"); })
              .on("mousemove", mousemove);
           
              function mousemove() {
                  var x0 = x.invert(d3.mouse(this)[0]),
                      i = bisectDate(dataFilter, x0, 1),
                      d0 = dataFilter[i - 1],
                      d1 = dataFilter[i],
                      d = x0 - d0.ds > d1.ds - x0 ? d1 : d0;
                  focus.attr("transform", "translate(" + x(d.ds) + "," + y(d.price) + ")");
                  chicken_tooltip.attr("style", "left:" + (x(d.ds) +100) + "px;top:"+ (y(d.price)+300) + "px;"  );
                  chicken_tooltip.select(".tooltip-date").text(dateFormatter(d.ds));
                  chicken_tooltip.select(".tooltip-likes").text(formatValue(d.price));
              }
     

            
        }
    
        // When the button is changed, run the updateChart function
        d3.select("#selectButton").on("change", function(d) {
            // recover the option that has been chosen
            var selectedOption = d3.select(this).property("value")
            // run the updateChart function with this selected option
            update(selectedOption)
        })
    })