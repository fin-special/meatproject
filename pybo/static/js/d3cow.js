
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 100, bottom: 30, left: 50},
        width = 960 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var container = d3.select("#cow")
      .append("svg")
        // .attr("width", width + margin.left + margin.right)
        // .attr("height", height + margin.top + margin.bottom)
        .attr("viewBox", '0 0 900 400')
      .append("g")
        .attr("class","cw")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // append the div for tooltip object
    var cow_tooltip = d3.select("#cow").append("div")
            .attr("class", "tooltip")
            .style("display", "none");
    //Read the data
    
    d3.json("./static/json/cow_predict_price.json", function(data) {
      
        
        var parseDate = d3.timeParse("%Y-%m-%d");
            bisectDate = d3.bisector(function(d) { return d.ds; }).left,
            formatValue = d3.format(",")
            dateFormatter = d3.timeFormat("%m/%d/%y");
    
        // 날짜형식 parser
        data.forEach(function(d) {
          d.ds = parseDate(d.ds);
          // 가격 소수점 제거
          d.yhat = parseInt(d.yhat);
        });

       
        // A color scale: one color for each group
        var myColor = d3.scaleOrdinal()
          .domain("yhat")
          .range(d3.schemeSet2);

        
        // Add X axis --> it is a date format
        var x = d3.scaleTime()
            .domain([data[0].ds, data[data.length - 1].ds])
            .range([0, width])
        svg = d3.selectAll("g.cw")
        svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x)
                  .tickFormat(dateFormatter));
        
        
        // Add Y axis
        var y = d3.scaleLinear()
          .domain( [d3.min(data.map(function(d){
                return d.yhat - 500
            })), d3.max(data.map(function(d){
                return d.yhat + 500
            }))])
          .range([ height, 0 ]);
        svg.append("g")
          .attr("class", "y axis")
          .call(d3.axisLeft(y));
    
        
        // draw a line
        svg
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
          
        
        // append hovering mousecursor circle
        var focus = svg.append("g")
            .attr("class", "focus")
            .style("display", "none");

            focus.append("circle")
                .attr("r", 5);
       
            //tooltipDate
             cow_tooltip.append("div")
                .attr("class", "tooltip-date");
    
            var tooltipLikes = cow_tooltip.append("div");
            tooltipLikes.append("span")
                .attr("class", "tooltip-title")
                .text("Price: ");
            //tooltip-likes
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
                focus.attr("transform", "translate(" + x(d.ds) + "," + y(d.yhat) + ")");
                cow_tooltip.attr("style", "left:" + (x(d.ds) +500) + "px;top:"+ (y(d.yhat) +200) + "px;" );
                cow_tooltip.select(".tooltip-date").text(dateFormatter(d.ds));
                cow_tooltip.select(".tooltip-likes").text(formatValue(d.yhat));
            }
        });

    
    