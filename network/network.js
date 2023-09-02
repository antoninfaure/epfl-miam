fetch(`./network/edges.json`)
    .then(response => {
        if (response.status == 404) throw error;
        return response.json();
    })
    .then(links => {
        fetch(`./network/vertices.json`)
            .then(response => {
                if (response.status == 404) throw error;
                return response.json();
            })
            .then(nodes => {
                const title = 'Menus ingredients'
                const width = $('#mynetwork').innerWidth()
                const height = $('#mynetwork').innerHeight()

                var initial_zoom = d3.zoomIdentity.translate(600, 400).scale(0.001);

                //add zoom capabilities 
                var zoom_handler = d3.zoom().on("zoom", zoom_actions);

                const svg = d3.select('#mynetwork')
                    .attr('width', width)
                    .attr('height', height)
                    .call(zoom_handler)
                    .call(zoom_handler.transform, initial_zoom)

                var max_value = 0
                for (node of nodes) {
                    if (node.size > max_value) max_value = node.size;
                }

                var color = d3.scaleLinear()
                    .domain([1, max_value])
                    .range(["yellow", "red"])

                const radius = 10

                var k = nodes.map(d => d.size).reduce((a, b) => a + b, 0) / nodes.length
                console.log(k)

                var simulation = d3.forceSimulation()
                    .force("link", d3.forceLink().id(function (d) { return d.id; }))
                    .force("center", d3.forceCenter(width / 2, height / 2))
                    .force("collide", d3.forceCollide().radius(d => { return d.size * 2 * radius }).iterations(3))
                    .on("tick", ticked);


                var zoomable = svg.append("g").attr("class", "zoomable").attr('transform', initial_zoom),
                    link = zoomable.append("g").attr('class', 'links').selectAll(".link"),
                    node = zoomable.append("g").attr('class', 'nodes').selectAll(".node")


                // Create a drag handler and append it to the node object instead
                var drag_handler = d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended);

                restart()

                // TITLE
                svg.append('g')
                    .append('text')
                    .attr('class', 'title')
                    .attr('x', width / 2)
                    .attr('y', 50)
                    .attr('text-anchor', 'middle')
                    .text(title);

                /// RESTART WHEN CHANGE OF DATA
                function restart() {
                    node.remove()
                    link.remove()

                    link = zoomable.append("g").attr('class', 'links').selectAll(".link"),
                        node = zoomable.append("g").attr('class', 'nodes').selectAll(".node")

                    node = node.data(nodes, function (d) { return d.id }).call(function (a) {
                        a.transition().attr("r", function (d) {
                            return d.size * radius
                        })
                            .attr("fill", function (d) {
                                return color(d.size);
                            })
                    })

                    var selection = node.enter().append('g').attr('class', 'node')

                    selection.append("circle")
                        .call(function (node) {
                            node.transition().attr("r", function (d) {
                                return d.size * radius
                            })
                                .attr("fill", function (d) {
                                    return color(d.size);
                                })
                        })


                    selection.append("text")
                        .attr('class', 'text-label')
                        .attr("text-anchor", "middle")
                        .attr("dy", ".35em")
                        .text(function (d) {
                            return d.label
                        })
                        .style("font-size", function (d) {
                            return d.size * radius
                        })
                        .style('fill', 'black')

                    node = selection.merge(node)

                    // Apply the general update pattern to the links.
                    link = link.data(links, function (d) { return d.source.id + "-" + d.target.id; });
                    link.exit().remove();
                    link = link.enter().append("g").append("line")
                        .call(function (link) {
                            link.transition()
                                .attr("stroke-opacity", 1)
                                .attr("stroke-width", function (d) { return d.size*2 + 'px' })
                        })
                        .style('stroke', 'black').merge(link);

                    drag_handler(node);

                    simulation.nodes(nodes)

                    simulation.force("link").links(links);

                    simulation.alphaTarget(0.3).restart();
                    d3.timeout(function () {
                        simulation.alphaTarget(0);
                    }, 500)


                }

                /* ----------------- */
                /* UTILITY FUNCTIONS */
                /* ----------------- */

                // EACH SIMULATION TICK
                function ticked() {
                    link
                        .attr("x1", function (d) { return d.source.x; })
                        .attr("y1", function (d) { return d.source.y; })
                        .attr("x2", function (d) { return d.target.x; })
                        .attr("y2", function (d) { return d.target.y; });

                    node
                        .attr("transform", function (d) {
                            return "translate(" + d.x + "," + d.y + ")";
                        })
                }

                function dragstarted(d) {
                    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }

                function dragged(d) {
                    d.fx = d3.event.x;
                    d.fy = d3.event.y;
                }

                function dragended(d) {
                    if (!d3.event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }

                function zoom_actions() {
                    if (zoomable) {
                        zoomable.attr("transform", d3.event.transform)
                    }
                }

                fetch(`./network/bigrams.json`)
                    .then(response => {
                        if (response.status == 404) throw error;
                        return response.json();
                    })
                    .then(bigrams => {
                        // List top 50 bigrams in #topbigrams
                        var topbigrams = bigrams.sort((a, b) => b[1] - a[1]).slice(0, 50)
                        $('#topbigrams').empty()
                        $('#topbigrams').append('<ul>')
                        for (let bigram of topbigrams) {
                            $('#topbigrams').append(`<li>${bigram[0][0]}, ${bigram[0][1]} (${bigram[1].toFixed(0)})</li>`)
                        }
                        $('#topbigrams').append('</ul>')
                    })
                    .catch(err => {
                        console.error(err)
                        console.error("No data for bigrams")
                    })
            })
            .catch(err => {
                console.error(err)
                console.error("No data for vertices")
            })
    })
    .catch(err => {
        console.error(err)
        console.error("No data for edges")
    })

