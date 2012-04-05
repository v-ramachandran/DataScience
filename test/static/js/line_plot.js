debug = false;
d3.csv("preprocessed-data/partyTrends.csv", function handleCSV(csv) {
  var demdata = csv.filter(function(el) { return el.party == "D" })
            .map(function(el) { return parseInt(el.contb_receipt_amt); });
  var repdata = csv.filter(function(el) { return el.party == "R" })
            .map(function(el) { return parseInt(el.contb_receipt_amt); });
  var libdata = csv.filter(function(el) { return el.party == "L" })
            .map(function(el) { return parseInt(el.contb_receipt_amt); });
  var months = csv.filter(function(el) { return el.party == "D" })
            .map(function(el) { return el.contb_receipt_dt; });
  var points = new Array();
  
  for (var i = 0; i < 12; i++) {
    //if (i==0) {
    points [i] = {m: months[i], d: demdata[i], l: libdata[i], r:repdata[i]};
    //} else {
    //points [i] = {m: months[i], d: demdata[i]+points[i-1].d, l: libdata[i]+points[i-1].l, r:repdata[i]+points[i-1].r};    
    //}
  }
  if (debug) { 
    console.log(points);
  }

  var p = 20,
      w = 275 - 2 * p,
      h = 225 - 2 * p,
      r=1.5,
      labelpad=-10,
      m = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
      ymax = 45000000,
      ymin = 0;
  
  var x = d3.scale.ordinal()
                  .domain(m);

  x.rangePoints([0,235]);

  var y = d3.scale.linear()
                  .domain([ymin, ymax])
                  .range([h, 0]);
  
  if (debug) {
    console.log(x("FEB"));
  }

  var vis = d3.select("div #line")
              .data([points])
              .append("svg")
              .attr("width", w + p * 2)
              .attr("height", h + p * 2)
              .append("g")
              .attr("transform", "translate(" + p + "," + p + ")");

  // Draw points


  // Draw Lines
  vis.append("svg:path")
         .attr("fill", "red")
         .attr("stroke", "red")
         .attr("stroke-width", 2)
         .attr("opacity", ".7")
         .attr("d", d3.svg.area()
           .x(function(d) { return x(d.m); })
           .y0(h)
           .y1(function(d) {return y(d.d+d.l+d.r); }));
  vis.append("svg:path")
         .attr("fill", "darkblue")
         .attr("stroke", "darkblue")
         .attr("stroke-width", 2)
         .attr("opacity", ".9")
         .attr("d", d3.svg.area()
           .x(function(d) { return x(d.m);})
           .y0(h)
           .y1(function(d) {return y(d.d+d.l); }));
  vis.append("svg:path")
         .attr("fill", "#ffcc00")
         .attr("stroke", "#ffcc00")
         .attr("stroke-width", 2)
         .attr("opacity", ".7")
         .attr("d", d3.svg.area()
           .x(function(d) { return x(d.m); })
           .y0(h)
           .y1(function(d) {return y(d.l); }));

  // Draw axes
  var temp = vis.selectAll("circle")
     .data(points)
     .enter();
  temp.append("circle")
     .attr("cx", (function(d) {return x(d.m); }))
     .attr("cy", (function(d) {return y(d.d); }))     
     .attr("r", r)
     .attr("fill", "#ffcc00");
  temp.append("circle")
     .attr("cx", (function(d) {return x(d.m); }))
     .attr("cy", (function(d) {return y(d.l+d.d); }))
     .attr("r", r)
     .attr("fill", "darkblue");
  temp.append("circle")
     .attr("cx", (function(d) {return x(d.m); }))
     .attr("cy", (function(d) {return y(d.r+d.l+d.d); }))
     .attr("r", r)
     .attr("fill", "red");
     
    var xrule = vis.selectAll("g.xrule")
                 .data(y.ticks(7))
                 .enter()
                 .append("svg:g")
                 .attr("class", "xrule")
                 .attr("transform", function(d) { return "translate(0,"+y(d)+")"; });

    xrule.append("line")
       .attr("y1", 0)
       .attr("y2", 0)
       .attr("x1", 0)
       .attr("x2", w+2)
       .attr("stroke", "#777")
       .attr("stroke-opacity", ".25");

    xrule.append("text")
       .attr("x", labelpad)
       .attr("text-anchor", "end")
       .attr("font-size", "9px")
       .text(function(d, i) {if (i==0) return d; else return d/1000000 ;});
    var yrule = vis.selectAll("g.yrule")
                 .data(m)
                 .enter()
                 .append("svg:g")
                 .attr("class", "yrule")
                 .attr("transform", function(d) { return "translate("+x(d)+",0)"; });
    yrule.append("line")
       .attr("y1", h+10)
       .attr("y2", h+2)
       .attr("x1", 0)
       .attr("x2", 0)
       .attr("stroke", "#777")
       .attr("stroke-opacity", ".25");

    yrule.append("text")
       .attr("y", h+16)
       .attr("dx", -10)
       .attr("font-size", "8px")
       .text(function(d, i) {return m[i];});     
    
    vis.append("svg:rect")
      .attr("x", w - 65)
      .attr("y", 3)
      .attr("fill", "darkblue")
      .attr("stroke", "darkblue")
      .attr("opacity", ".7")
      .attr("height", 5)
      .attr("width", 10);
    vis.append("svg:text")
      .attr("x", -45 + w)
      .attr("y", 8)
      .attr("font-size", "8.5px")
      .text("Democrat");
    vis.append("svg:rect")
      .attr("x", w - 65)
      .attr("y", 13)
      .attr("fill", "red")
      .attr("stroke", "red")
      .attr("opacity", ".7")
      .attr("height", 5)
      .attr("width", 10);
    vis.append("svg:text")
      .attr("x", -45 + w)
      .attr("y", 18)
      .attr("font-size", "8.5px")
      .text("Republican");
    vis.append("svg:rect")
      .attr("x", w - 65)
      .attr("y", 23)
      .attr("fill", "#ffaa00")
      .attr("stroke", "#ffaa00")
      .attr("opacity", ".7")
      .attr("height", 5)
      .attr("width", 10);
    vis.append("svg:text")
      .attr("x", -45 + w)
      .attr("y", 28)
      .attr("font-size", "8.5px")
      .text("Libertarian");

});

