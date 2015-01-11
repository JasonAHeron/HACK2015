function updateSessions() {
	console.log( "Update Sessions" );
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		if ( xmlhttp.readyState == 4 && xmlhttp.status == 200 ) {
			var data = xmlhttp.response;
			var pendingList = $('#sessions').find('.pendingSess');
			var scheduledList = $('#sessions').find('.scheduledSess');
			pendingList.empty();
			scheduledList.empty();
			data.forEach( function( item ) {
				li = $('<li></li>').addClass( 'text-mutedSession' ).text( item['name'] );
				if ( item['session'] == null )
					pendingList.append( li );
				else
					scheduledList.append( li );
			} );
		}
	}
	xmlhttp.open( 'GET', 'rest?action=update', true );
	xmlhttp.responseType = 'json'
	xmlhttp.send();
}

$(document).ready( updateSessions );