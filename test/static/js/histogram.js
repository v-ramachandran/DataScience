d3.csv("preprocessed-data/partySplits.csv", function handleCSV(csv) {
  // select revenues of CA companies
  
  var data = csv.map(function(el) {return parseFloat(el.contb_receipt_amt) }),
      party = csv.map(function(el) {return (el.party) }),
      w = 235,
      h = 185,
      r = Math.min(w, h) / 1.75,
      p = 20,
      parties = ["D","L", "R"],
      color = ["blue", "yellow", "red"],
      total = data[0]+data[1]+data[2]
      //color = d3.scale.category20(),
      donut = d3.layout.pie(),
      arc = d3.svg.arc().innerRadius((r * .5) - 5).outerRadius(r-5);
  var pos = d3.svg.arc().innerRadius(r + 5).outerRadius(r + 5); 
  var vis = d3.select("div #histogram")
      .append("svg")
      .data([data])
      .attr("width", w + p * 2)
      .attr("height", w + p * 2);

  var arcs = vis.selectAll("g.arc")
      .data(donut)
      .enter().append("g")
      .attr("class", "arc")
      .attr("transform", "translate(" + (2.5*p+r) + "," + (.75*p+r)+ ")");

  arcs.append("path")
      .attr("fill", function(d, i) { return color[i]; })
      .attr("d", arc);
  arcs.append("text")
      .attr("transform", function(d) { return "translate(" + pos.centroid(d) + ")"; })
      .attr("text-anchor", "middle")
      .text(function(d, i) { return parties[i]; });

  // Append central text
  arcs.append("text")
      .attr("id", "temp")
      .attr("text-anchor", "middle");
      
      var t = d3.select("#temp");
      
      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "-.5em")
      .text(function(d) { return "Total" });
      
      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "2.5em")
      .text(function(d) { return "$ "+total.toFixed(2); });
  
  arcs.on("mouseover", function(d, i){
      
      d3.select("#temp").remove();
      d3.select(this).append("text")
      .attr("transform", function(d) { return "translate(" + (arc.centroid(d)*1.5) + ")"; })
      .attr("dy", ".1em")
      .attr("id", "temp")
      .attr("text-anchor", "middle");
      
      var t = d3.select("#temp");

      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "-.5em")
      .text(function(d) { return party[i]; });
      
      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "2.5em")
      .text(function(d) { return "$ "+d.value.toFixed(2); });
      
      })
      .on("mouseout", function(d, i){
      
      d3.select("#temp").remove();
      d3.select(this).append("text")
      .attr("dy", ".1em")
      .attr("id", "temp")
      .attr("text-anchor", "middle");
      
      var t = d3.select("#temp");
      
      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "-.5em")
      .text(function(d) { return "Total" });
      
      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "2.5em")
      .text(function(d) { return "$ "+total.toFixed(2); });    
      });
})
