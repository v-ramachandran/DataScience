d3.csv("preprocessed-data/cloro.csv", function handleCSV(csv) {
    var rfracs = csv.map(function(el) {return parseInt(el.r); }),
        dfracs = csv.map(function(el) {return parseInt(el.d); }),
        stlist = csv.map(function(el) {return el.contbr_st;});
    console.log("Goes here.");
    for (var i=0; i<stlist.length; i++) {
        state = stlist[i]
        id = '#'+state;
        fill="black";
        if (rfracs[i]==1){
          fill="darkred";
        } else {
          fill="darkblue";
        }
        try {
        d3.select(id).attr("fill", fill)
                     .attr("opacity", ".85");
        } catch (e) {        
        }
    }
    var w=959;
    var vis = d3.select("#svg2");
        vis.append("svg:rect")
        .attr("x", w - 225)
        .attr("y", 83)
        .attr("fill", "darkblue")
        .attr("stroke", "darkblue")
        .attr("opacity", ".7")
        .attr("height", 5)
        .attr("width", 10);
    vis.append("svg:text")
        .attr("x", -205 + w)
        .attr("y", 88)
        .attr("font-size", "9px")
        .text("Democrat");
    vis.append("svg:rect")
        .attr("x", w - 225)
        .attr("y", 93)
        .attr("fill", "darkred")
        .attr("stroke", "darkred")
        .attr("opacity", ".7")
        .attr("height", 5)
        .attr("width", 10);
    vis.append("svg:text")
        .attr("x", -205 + w)
        .attr("y", 98)
        .attr("font-size", "9px")
        .text("Republican");
});
