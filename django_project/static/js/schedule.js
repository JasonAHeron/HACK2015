function scheduleInit() {
	var schedules = document.getElementsByClassName( "schedule" );
	for ( i = 0; i < schedules.length; ++i ) {
		var table = document.createElement( "table" );
		schedules.item( i ).appendChild( table );
		var tr = document.createElement( "tr" );
		tr.innerHTML = "<th>&nbsp;</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th>";
		table.appendChild( tr );
		for ( i = 0; i < 48; ++i ) {
			tr = document.createElement( "tr" );
			var hours = Math.floor( i/2 )%12;
			if ( hours == 0 ) hours += 12;
			if ( hours < 10 ) hours = "0" + hours;
			var td = document.createElement( "th" );
			td.innerHTML = hours + ':' + ( i%2 ? '3' : '0' ) + "0 " + ( i < 24 ? 'A' : 'P' ) + 'M'+"&nbsp;";
			tr.appendChild( td );
			for ( j = 0; j < 7; ++j ) {
				td = document.createElement( "td" );
				tr.appendChild( td );
				var draggable = document.createElement( "div" );
				draggable.innerHTML = "&nbsp;";
				draggable.setAttribute( "draggable", "true" );
				draggable.onmouseup = function(e){ onScheduleMouseUp( e ); }
				draggable.ondragstart = function(e){ onScheduleDragStart( e ); }
				draggable.ondragend = function(e){ onScheduleDragEnd( e ); }
				draggable.ondragover = function(e){ onScheduleDragOver( e ); }
				draggable.ondrop = function(e){ event.preventDefault(); }
				draggable.col = j;
				draggable.row = i;
				td.appendChild( draggable );
			}
			table.appendChild( tr );
		}
	}
}

var schedule_dragging = false;
var schedule_table = null;
var schedule_drag_col = 0;
var schedule_drag_row = 0;
var schedule_drag_row_to = 0;

function onScheduleDragStart( e ) {
	schedule_dragging = true;
	var cell = e.target.parentNode;
	if ( e.dataTransfer != null ) {
		e.dataTransfer.dropEffect = "none";
	}
	schedule_table = cell.parentNode.parentNode;
	schedule_drag_col = e.target.col;
	schedule_drag_row = e.target.row;
	schedule_drag_row_to = e.target.row;
	cell.setAttribute( "class", "selected" );
}

function onScheduleDragEnd( e ) {
	console.log( "Drag End" );
	schedule_dragging = false;
	var highlight = !e.target.parentNode.highlighted;
	var from = 0;
	var to = 0;
	if ( schedule_drag_row_to < schedule_drag_row ) {
		from = schedule_drag_row_to;
		to = schedule_drag_row;
	} else {
		from = schedule_drag_row;
		to = schedule_drag_row_to;
	}
	for ( i = from; i <= to; ++i )
		schedule_table.childNodes[ i + 1 ].childNodes[ schedule_drag_col + 1 ].highlighted = highlight;
	scheduleColorCells( from, to, false );
	event.preventDefault();
}

function onScheduleDragOver( e ) {
	event.preventDefault();
	var m = e.target.row;
	if ( m == schedule_drag_row_to ) return false;
	if ( schedule_drag_row_to < schedule_drag_row && m > schedule_drag_row ) {
		scheduleColorCells( schedule_drag_row_to, schedule_drag_row - 1, false );
		schedule_drag_row_to = schedule_drag_row;
	} else if ( schedule_drag_row_to > schedule_drag_row && m < schedule_drag_row ) {
		scheduleColorCells( schedule_drag_row + 1, schedule_drag_row_to, false );
		schedule_drag_row_to = schedule_drag_row;
	}
	if ( m > schedule_drag_row_to ) {
		if ( schedule_drag_row_to >= schedule_drag_row )
			scheduleColorCells( schedule_drag_row_to + 1, m, true );
		else
			scheduleColorCells( schedule_drag_row_to, m - 1, false );
		schedule_drag_row_to = m;
	} else if ( m < schedule_drag_row_to ) {
		if ( schedule_drag_row_to <= schedule_drag_row )
			scheduleColorCells( m, schedule_drag_row_to - 1, true );
		else
			scheduleColorCells( m + 1, schedule_drag_row_to, false );
		schedule_drag_row_to = m;
	}
	return false;
}

function onScheduleMouseUp( e ) {
	console.log( "MouseUp" );
	if ( !schedule_dragging ) {
		onScheduleDragStart( e );
		onScheduleDragEnd( e );
	}
}

function scheduleColorCells( from, to, select ) {
	for ( ; from <= to; ++from ) {
		var cell = schedule_table.childNodes[ from + 1 ].childNodes[ schedule_drag_col + 1 ];
		if ( select ) cell.setAttribute( "class", "selected" )
		else if ( cell.highlighted ) cell.setAttribute( "class", "highlighted" )
		else cell.removeAttribute( "class" )
	}
};

function scheduleGetData(	schedule ) {
	schedule = schedule.childNodes[ 0 ]
	var date = new Date();
	date.setHours( 0, 0, 0, 0 );
	while ( date.getDay() > 0 )
		date.setDate( date.getDate() - 1 )
	dict = {};
	for ( i = 0; i < 7; ++i ) {
		var on = false;
		var periods = [];
		for ( j = 0; j < 48; ++j ) {
			var highlighted = schedule.childNodes[ j + 1 ].childNodes[ i + 1 ].highlighted
			if ( highlighted && !on ) {
				on = true;
				periods.push( j );
			} else if ( !highlighted && on ) {
				on = false;
				periods.push( j );
			}
		}
		if ( on ) periods.push( 47 );
		dict[ date.getTime() ] = periods;
		date.setDate( date.getDate() + 1 );
	}
	return dict;
}
