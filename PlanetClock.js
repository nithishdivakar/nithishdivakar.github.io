var PlanetClock = (function(){

	var Config ={
		orbit_radius    :350,
		orbit_thickness :6,
		dial_element    :"circle",
		dial_width      :12,
		dial_height     :0,  //might be useful later
		TimeOffset      :0,
	};

	var clock_container;

	var TimeRange = {start:0, end:24*60*60};

	var arcOrbit  = d3.svg.arc()
		.startAngle( function(d) { return timeToAngle(d.start); })
		.endAngle(   function(d) { return timeToAngle(d.end);   })
		.innerRadius(function(d) { return Config.orbit_radius;})
		.outerRadius(function(d) { return Config.orbit_radius + Config.orbit_thickness;});
	
	
	var setTimeRange = function(s, e){
		animate(TimeRange.start,s,TimeRange.end,e);
		// then fininsh off by setting actual value.
		TimeRange.start = s;
		TimeRange.end   = e;
		redraw();
	}
	
	var animate = function(s1,s2,e1,e2) {
		clock_container
		.transition()
		.duration(1000)
		.styleTween("color",function(){
			var sd = d3.interpolateNumber(s1,s2);
			var ed = d3.interpolateNumber(e1,e2);
	
			return function(t) {
				TimeRange.start = sd(t);
				TimeRange.end   = ed(t);
				redraw();
			};
		});
	}
	
	
	
	
	var timeToAngle = function(TimeofDay){
		var t = Math.max(TimeRange.start,TimeofDay);
		t     = Math.min(TimeRange.end  ,t);
		return (t-TimeRange.start)/(TimeRange.end - TimeRange.start) *2*Math.PI + Config.TimeOffset;
	}
	
	var timeOfDay = function(){
		d = new Date;
		var second = d.getSeconds();
		var minute = d.getMinutes();
		var hour   = d.getHours() ;
		var secondOftheDay = hour*60*60 + minute*60 + second;
		//secondOftheDay=(secondOftheDay*1000)%(24*60*60);
		return {
	hour :hour, 
		 minute:minute, 
		 second:second, 
		 tot_sec:secondOftheDay
		};
	}
	
	var putDialOnOrbit = function(now, start, end){
		var t = Math.max(start,now);
		t     = Math.min(end  ,t);
	
		Q = (t-start)/(end-start)*2*Math.PI  -Math.PI/2 + Config.TimeOffset;
		R = Config.orbit_radius + Config.orbit_thickness/2;
		return "translate(" +R*Math.cos(Q)+ "," +R*Math.sin(Q) +")";
	}
	
	var init_dial = function(clock_container){
		var dial_container = clock_container.append("g").attr("id","dial-group");
	
		dial_container.append(Config.dial_element).attr("id","dial-element");
		dial_container.append("text").attr("id","dial-text");
	
		dial_container.selectAll(Config.dial_element)
			.attr("r",Config.dial_width)
			.attr("fill", "#fff");
	
		dial_container.selectAll("text")
			.attr("style","font-size:xx-small")
			.attr("transform", "translate(-11,3)");
	
	}
	
	var init_orbit = function(clock_container){
		var orbit_container = clock_container.append("g").attr("id","orbit-group");
		orbit_container.append("path").attr("id","completed");
		orbit_container.append("path").attr("id","notcompleted");
	
	
	
		orbit_container.selectAll("path")
			.data([{start:0,end:24},{start:24,end:24}])
			.attr("d",arcOrbit)
			.attr("stroke","rgba(0,0,0,0)")
			.attr("style","stroke:rgba(0,0,0,0)")
			.attr("fill", function(d) { if(d.start == TimeRange.start) return "#999"; else return "#111"; })
			.attr("fill-rule","nonzero")
			.attr("fill-opacity","0.4")
			;
	}
	
	var redraw_dial = function(dial_container, X){
		var TIME = X.tot_sec;
		var H = X.hour;
		var M = X.minute;
	
	
		dial_container.attr("transform",putDialOnOrbit(TIME,TimeRange.start,TimeRange.end));
		dial_container.selectAll("text").text(""+H+":"+M);
	}
	
	var redraw_orbit = function(orbit_container,X){
		var TIME  = X.tot_sec;
		var start = Math.min(TimeRange.start,TIME);
		var end   = Math.max(TimeRange.end  ,TIME);
		var Data = [{start:start,end:TIME},{start:TIME,end:end}];
		orbit_container.selectAll("path").data(Data).attr("d",arcOrbit);
	
	}
	
	var redraw = function(){
		var X = timeOfDay();
		redraw_orbit(clock_container.select("g#orbit-group"),X);
		redraw_dial (clock_container.select("g#dial-group"),X);
	}
	
	var create = function(C){
	
		clock_container = C;
		init_orbit(clock_container);
		init_dial (clock_container);
	
		redraw();
		setInterval(redraw,60000);
	
	}
	
	var set = function(id,val){
		Config[id] = val;
		redraw();
	}
	
	return {
		create:create,
		redraw:redraw,
		set:set,
		setTimeRange:setTimeRange
	};
})();
