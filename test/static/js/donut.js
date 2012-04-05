d3.csv("preprocessed-data/partySplits.csv", function handleCSV(csv) {
  // select revenues of CA companies
  
  var data = csv.map(function(el) {return parseFloat(el.contb_receipt_amt) }),
      party = csv.map(function(el) {return (el.party) }),
      w = 235,
      h = 185,
      r = Math.min(w, h) / 1.75,
      p = 20,
      o = ".65",
      wt = "900",
      parties = ["D","L", "R"],
      color = ["darkblue", "#ffcc00", "rgb(255,0,0)"],
      total = data[0]+data[1]+data[2]
      //color = d3.scale.category20(),
      donut = d3.layout.pie(),

      arc = d3.svg.arc().innerRadius((r * .5) - 3).outerRadius(r-5);
  var pos = d3.svg.arc().innerRadius(r + 5).outerRadius(r + 5); 
  var vis = d3.select("div #donut")
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
      .attr("opacity", o)
      .attr("d", arc)
      .attr("stroke", function(d, i) { return color[i]; })
      .attr("stroke-width", ".5")
      .on("mouseover", function (d) { d3.select(this).attr("opacity", "1").attr("stroke-width", function(d, i) { if (i==1) return "10"; else return ".5"; });})    
      .on("mouseout", function (d) { d3.select(this).attr("opacity", o).attr("stroke-width", ".5");});
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
      .attr("font-weight", wt)
      .attr("x", "0")
      .attr("dy", "-.5em")
      .text(function(d) { return "Total" });
      
      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "2.5em")
      .text(function(d) { return "$ "+total.toFixed(0); });
  
  arcs.on("mouseover", function(d, i){
      
      d3.select("#temp").remove();
      d3.select(this).append("text")
      .attr("dy", ".1em")
      .attr("id", "temp")
      .attr("text-anchor", "middle");
      
      var t = d3.select("#temp");

      t.append("tspan")
      .attr("font-weight", wt)
      .attr("x", "0")
      .attr("dy", "-.5em")
      .text(function(d) { return party[i]; });
      
      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "2.5em")
      .text(function(da) { return ((d.value/total)*100).toFixed(1); });
      
      })
      .on("mouseout", function(d, i){
      
      d3.select("#temp").remove();
      d3.select(this).append("text")
      .attr("dy", ".1em")
      .attr("id", "temp")
      .attr("text-anchor", "middle");
      
      var t = d3.select("#temp");
      
      t.append("tspan")
      .attr("font-weight", wt)
      .attr("x", "0")
      .attr("dy", "-.5em")
      .text(function(d) { return "Total" });
      
      t.append("tspan")
      .attr("x", "0")
      .attr("dy", "2.5em")
      .text(function(d) { return "$ "+total.toFixed(0); });    
      });
})
