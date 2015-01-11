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
			var i = 0;
			data.forEach( function( item ) {
			//create buttons to skip session or delete session
			var element=document.createElement("button");
			element.type='button';
            element.value='buttonDelete'+i;
			element.name='buttonDelete' + i;
			element.innerHTML='Cannot Make Session This Week';
			element.setAttribute('class','edit leaveGroupBtn');
			element.style.width="200px";
			//but.setAttribute("onclick",callJavascriptFunction);
			//working here
/*but.onclick= callJavascriptFunction;
document.getElementById("but").onclick=callJavascriptFunction;*/
			var mybr = document.createElement('br');



				//create accordion
				var title = $('<a></a>')
					.addClass( 'accordion-section-title' )
					.attr( 'href', '#accordion-' + i )
					.text( item['name'] )
					.click( function(e) {
						if( $(this).is('.active') ) close_accordion_section();
						else {
							close_accordion_section();
							$(this).addClass('active');
							$($(this).attr('href')).slideDown(300).addClass('open'); 
						}

						e.preventDefault();
					} );
				var content = $('<div></div>').addClass( 'accordion-section-content' ).attr( 'id', 'accordion-' + i ).attr( 'style', 'display: none;' )
					.append( $('<p></p>').text( 'Lorem Ipsum' ).append(mybr).append(element) );
				//if section is recurring, show extra button
				var test=1;
				if(test==1){
				   	var btn1=document.createElement("button");
					btn1.type='button';
            		btn1.value='buttonRecur'+i;
					btn1.name='buttonRecur' + i;
					btn1.innerHTML='Delete Session Permanently';
					btn1.style.width="200px";
					btn1.setAttribute('class','edit deleteGroupBtn');
					content.append(btn1);

				}
				var li = $('<li></li>').addClass( 'accordion-section' ).append( title ).append( content );
				//li = $('<li></li>').addClass( 'text-mutedSession' ).text( item['name'] );
				if ( item['session'] == null )
					pendingList.append( li );
				else
					scheduledList.append( li );
				++i;
			} );
		}
	}
	xmlhttp.open( 'GET', 'rest?action=update', true );
	xmlhttp.responseType = 'json'
	xmlhttp.send();
}
function close_accordion_section() {
	$('.accordion-section .accordion-section-title').removeClass('active');
	$('.accordion-section .accordion-section-content').slideUp(300).removeClass('open');
}
$(document).ready( updateSessions );