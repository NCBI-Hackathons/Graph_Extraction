/*!
 *
 *  Web Starter Kit
 *  Copyright 2015 Google Inc. All rights reserved.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *    https://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License
 *
 */
/* eslint-env browser */
(function() {
 'use strict';

 // Check to make sure service workers are supported in the current browser,
 // and that the current page is accessed from a secure origin. Using a
 // service worker from an insecure origin will trigger JS console errors. See
 // http://www.chromium.org/Home/chromium-security/prefer-secure-origins-for-powerful-new-features
 var isLocalhost = Boolean(window.location.hostname === 'localhost' ||
		 // [::1] is the IPv6 localhost address.
		 window.location.hostname === '[::1]' ||
		 // 127.0.0.1/8 is considered localhost for IPv4.
		 window.location.hostname.match(
			 /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/
			 )
		 );

 if ('serviceWorker' in navigator &&
		 (window.location.protocol === 'https:' || isLocalhost)) {
 navigator.serviceWorker.register('service-worker.js')
 .then(function(registration) {
		 // updatefound is fired if service-worker.js changes.
		 registration.onupdatefound = function() {
		 // updatefound is also fired the very first time the SW is installed,
		 // and there's no need to prompt for a reload at that point.
		 // So check here to see if the page is already controlled,
		 // i.e. whether there's an existing service worker.
		 if (navigator.serviceWorker.controller) {
		 // The updatefound event implies that registration.installing is set:
		 // https://slightlyoff.github.io/ServiceWorker/spec/service_worker/index.html#service-worker-container-updatefound-event
		 var installingWorker = registration.installing;

		 installingWorker.onstatechange = function() {
		 switch (installingWorker.state) {
		 case 'installed':
		 // At this point, the old content will have been purged and the
		 // fresh content will have been added to the cache.
		 // It's the perfect time to display a "New content is
		 // available; please refresh." message in the page's interface.
		 break;

		 case 'redundant':
		 throw new Error('The installing ' +
				 'service worker became redundant.');

		 default:
		 // Ignore
		 }
		 };
		 }
		 };
 }).catch(function(e) {
	 console.error('Error during service worker registration:', e);
	 });
 }

 var width = 960,
     height = 500;

 var color = d3.scale.category20();

 //var force = d3.layout.force()
//	 .charge(-1)
//	 .linkDistance(30)
//	 .size([width, height]);
 var force = cola.d3adaptor()
    .linkDistance(30)
    .size([width, height]);

 var svg = d3.select("svg")
	 .attr("width", width)
	 .attr("height", height)
	 .style("pointer-events", "all");

 document.getElementById('fdgSelectorButton').onclick = function () {
	 d3.json(document.getElementById('fdgSelector').value, function(error, topgraph) {
			 if (error) throw error;

			 // Resolve the edges' source and target names
			 var nodelist = [];
			 topgraph.graphs[0].nodes.forEach( function(node) {
					 nodelist[node.id] = node;
					 });
			 topgraph.graphs[0].edges.forEach( function(edge) {
					 edge.source = nodelist[edge.source];
					 edge.target = nodelist[edge.target];
					 })
			 topgraph.graphs[0].edges = topgraph.graphs[0].edges.filter(function (t) {return typeof t.source !== 'undefined' && typeof t.target !== 'undefined'});

			 // Load into a force-directed D3 layout
			 force
			 .nodes(topgraph.graphs[0].nodes)
			 .links(topgraph.graphs[0].edges)
			 .start();


			 // Render the edges
			 var link = svg.selectAll(".link")
				 .data(topgraph.graphs[0].edges)
				 .enter().append("line")
				 .attr("class", "link")
				 .style("stroke-width", function(d) { return Math.sqrt(d.metadata.value); });

			 // Render the nodes first
			 var node = svg.selectAll(".node")
				 .data(topgraph.graphs[0].nodes)
				 .enter()
				 .append("g")
				 .attr("class", "node")
				 .call(force.drag);

			 node.append("circle")
				 .attr("r", 5)
				 .style("fill", function(d) { return color(d.metadata.group); });

			 node.append("text")
				 .text(function(d) { return d.label; })
				 .style("stroke", color(0)).style("stroke-width","0").style("font-family", "Arial").style("font-size", 12);

			// force.linkStrength(function(link) {
			//		 return 1-1/link.source.metadata.length;
			//		 });
			 svg.call(d3.behavior.zoom()
					 .translate([0, 0])
					 .scale(1.0)
					 .scaleExtent([0.5, 8.0])
					 .on("zoom", function() {
						 svg.attr("transform", "translate(" + d3.event.translate[0] + "," + d3.event.translate[1] + ") scale(" + d3.event.scale + ")")
						 })
				 )

			 // Force-directed layout functions
			 force.on("tick", function() {
					 link.attr("x1", function(d) { return d.source.x; })
					 .attr("y1", function(d) { return d.source.y; })
					 .attr("x2", function(d) { return d.target.x; })
					 .attr("y2", function(d) { return d.target.y; });

					 node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

					 });
	 });
 };
})();
