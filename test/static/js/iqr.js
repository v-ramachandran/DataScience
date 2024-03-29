
d3.csv("preprocessed-data/spreads.csv", function handleCSV(csv) {
  // select revenues of CA companies
  
    var tf = csv.map(function(el) {return parseInt(el.tf); }),
        median = csv.map(function(el) {return parseInt(el.median);}),
        sf = csv.map(function(el) {return parseInt(el.sf);}),
        namelist = csv.map(function(el) {return el.cand_nm;});
    var data = new Array();
    for (var i = 0; i < 12; i++) {
        data [i] = {tf: tf[i], median: median[i], sf: sf[i], name:namelist[i]};
    }
    var p = 20,
        w = 275 - 2 * p,
        h = 225 - 2 * p,
        xmin = 0,
        xmax = 3000,
        labelpad = 40,
        x = d3.scale.linear().domain([xmin, xmax]).range([0, w]),
        y = d3.scale.ordinal().domain(namelist).rangeBands([0, h], .2);

    var vis = d3.select("div #iqr")
        .append("svg")
        .attr("width", w + p * 2)
        .attr("height", h + p * 2)
        .append("g")
        .attr("transform", "translate(" + p + "," + p + ")");

    var bars = vis.selectAll("g.bar")
        .data(data)
        .enter()
        .append("svg:g")
        .attr("transform", function(d, i) { return "translate(" + (labelpad) + "," + y(i) + ")"; });

        bars.append("svg:rect")
        .attr("opacity", ".5")        
        .attr("fill", function(d, i) { return "#999";} ) //Alternate colors
        .attr("width", function (d) {return (x(d.median)-x(d.tf));})
        .attr("height", y.rangeBand())
        .attr("transform", function (d) {return "translate(" + (x(d.tf)) +", 0)"});
        bars.append("svg:rect")
        .attr("opacity", ".5")
        .attr("fill", function(d, i) { return "#999";} ) //Alternate colors
        .attr("width", function (d) {return (x(d.sf)-(x(d.median)));})
        .attr("height", y.rangeBand())
        .attr("transform", function (d) {return "translate(" + x(d.median) +", 0)"});
        bars.append("svg:rect")
        .attr("fill", function(d, i) { return "red";} ) //Alternate colors
        .attr("width", x(6))
        .attr("height", y.rangeBand())
        .attr("transform", function (d) {return "translate(" + x(d.median-3) +", 0)"});  
        
        bars.append("svg:text")
        .attr("x", -9)
        .attr("y", 2 + y.rangeBand() / 2)
        .attr("dx", 8)
        .attr("dy", ".22em")
        .attr("text-anchor", "end")
        .text(function(d, i) { return namelist[i]; });
        
        var rules = vis.selectAll("g.rule")
        .data(x.ticks(10))
        .enter().append("svg:g")
        .attr("transform", function(d) {return "translate(" + x(d) + ",0)"; });

        rules.append("svg:line")
        .attr("y1", h-10)
        .attr("y2", h-5)
        .attr("x1", labelpad)
        .attr("x2", labelpad)
        .attr("stroke-opacity", .3)
        .attr("stroke", "black");

        rules.append("svg:line")
        .attr("y1", h-10)
        .attr("y2", h-5)
        .attr("x1", 3*labelpad/2)
        .attr("x2", 3*labelpad/2)
        .attr("stroke-opacity", .3)
        .attr("stroke", "black");
        
        rules.append("svg:text")
        .attr("y", h)
        .attr("x", labelpad)
        .attr("dy", ".71em")
        .attr("font-size", "9px")
        .attr("text-anchor", "middle")
        .text(x.tickFormat(10));
  }
)

