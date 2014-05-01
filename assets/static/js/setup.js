/**
 * @file setup.js
 * @author Joseph Ciurej
 * @date Spring 2014
 *
 * Container Module for Base Setup Logic for CS411 Project Pages
 *
 * @TODO
 */


// Helper Functions //

/**
 * @return gid The group identifier for the current page (only valid for the
 *  groups page).
 */
function getGroupID()
{
    return $( "meta[name=groupid]" ).attr( "content" );
}

/**
 * @return bhFinder A 'BloodHound' instance that queries the back-end handler
 *  at the given url for autocomplete information.
 */
function getBloodhoundForURL( _url )
{
	var replacefun = function( u, q ) { 
		return u + "?query=" + q + "&" + "group=" + getGroupID();
	};

	var bhFinder = new Bloodhound( {
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace( "value" ),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		remote: { url: _url, wildcard: "%QUERY", replace: replacefun },
	} );

	bhFinder.initialize();
	return bhFinder;
}

// Primary Entry Point //

/**
 * Main function for the 'setup.js' script file.
 */
function main()
{
	// Set Up Libraries //
	{
		// Setup the Editable Fields //
		addEditableToForms( "" )

		// Setup the Deadline List Modules //
		bindAsyncToDeadlines( "" )

		// Setup the Datetime Picker Modules //
		$( ".datetimepicker-form" ).datetimepicker( {minDate: Date.now()} );
		$( ".timepicker-form" ).datetimepicker( {pickDate: false} );

		// Setup the Select Modules //
		$( "select" ).selectpicker();
	}

	// Set up Autocomplete Fields ///
	{
		var typeahead_options = { hint: true, highlight: true, minLength: 2 };

		$( "#new_user_email" ).typeahead( typeahead_options,
			{ name: "emails", displaykey: "value", 
			source: getBloodhoundForURL("../get-users").ttAdapter() } );
		$( "#course_name" ).typeahead( typeahead_options,
			{ name: "groups", displaykey: "value", 
			source: getBloodhoundForURL("../get-courses").ttAdapter() } );
		$( "#deadline_name" ).typeahead( typeahead_options,
			{ name: "emails", displaykey: "value", 
			source: getBloodhoundForURL("../get-deadlines").ttAdapter() } );

		// TODO: Remove this example code.
		/*$( "#group_name" ).typeahead( { hint: true, highlight: true, minLength: 2 },
			{ name: "states", displaykey: "value", source: substringMatcher(states) } );*/
	}

	// Bind AJAX Requests to Fields //
	{
		// Setup the Google Authentication Button //
		$( "#google_auth" ).click( function() {
			$.post("google-auth-request", function(url) {
				window.location.replace(url);
			});
		} );

	    // Setup Group Page Modal Submission Buttons //
        $( "#add-member-submit" ).click( function () {
            var data1 = {};
            data1['group_id'] = getGroupID();

            // Input element has no ID tag defined 
            data1['user_email'] = $('#user_email').val();
            $.ajax({
                type: 'POST',
                url: '/add-member',
                data: {'data': JSON.stringify(data1)},
                success: function(msg) {
					console.log( msg );
                    $('#add-member-modal').modal('hide');

                    response = $.parseJSON( msg );

					// TODO: icon not updating
					addUserEntry( response["name"], response["email"], response["iconurl"] );
                },
                error: function(data) {
                    alert("Failed to add user to group.");
                }
            });
        });
        
        $( "#add-subgroup-submit" ).click( function () {
            var data1 = {};
            data1['group_id'] = getGroupID();

            // Input element has no ID tag defined 
            data1['group_name'] = $('#group_name').val();
            data1['group_description'] = $('#group_description').val();
            $.ajax({
                type: 'POST',
                url: '/add-subgroup',
                data: {'data': JSON.stringify(data1)},
                success: function(msg) {
                    $('#add-subgroup-modal').modal('hide');
                    //response = $.parseJSON( msg );
                    //addGroupEntry(response["id"], response["name"], response["maintainer"]);
                },
                error: function(data) {
                    alert("Failed to add subgroup.");
                }
            });
        });

        $( "#add-deadline-submit" ).click( function () {
            var data1 = {};
            data1['group_id'] = getGroupID();
            data1['name'] = $('#deadline_name').val();
            data1['deadline'] = $('#deadline_datetime').val();
            data1['notes'] = $('#deadline_notes').val();
            $.ajax({
                type: 'POST',
                url: '/add-deadline',
                data: {'data': JSON.stringify(data1) },
                success: function(msg) {
                    $('#add-deadline-modal').modal('hide');
					response = $.parseJSON( msg );
					// TODO: Update this functionality.
					addDeadlineEntry( response["id"], response["name"], response["group"], response["type"], 
						response["time"], response["notes"], response["can_edit"] );
                },
                error: function(data, text) {
                    alert("Failed to add deadline." + text);
                }
            });
        });

        $( "#add-course-submit" ).click( function () {
            var data1 = {};
            data1['course_name'] = $('#course_name').val();
            $.ajax({
                type: 'POST',
                url: '/add-course',
                data: {'data': JSON.stringify(data1) },
                success: function(msg) {
                    $('#add-course-modal').modal('hide');
                    response = $.parseJSON( msg );
                    addGroupEntry(response["id"], response["name"], response["maintainer"]);
                },
                error: function(data, text) {
                    alert("Failed to add course." + text);
                }
            });
        });

        $( "#schedule-send-submit" ).click( function () {
            var data1 = {};
            if ($('#meeting_times option:selected').attr('data-datetime'))
                data1['meeting_time'] = $('#meeting_times option:selected').attr('data-datetime');
            else
                data1['meeting_time'] = "Sometime, dude."

            data1['meeting_message'] = $('#meeting_message').val();
            data1['group_id'] = getGroupID();

            $.ajax({
                type: 'POST',
                url: '/send-email',
                data: {'data': JSON.stringify(data1) },
                success: function(msg) {
                    $('#schedule-send-modal').modal('hide');
                },
                error: function(data, text) {
                    alert("Failed to send email." + text);
                }
            });
        });

        $( "#schedule-query-submit" ).click( function () {
            var data1 = {};
            var members = [];
            $('#meeting_members option:selected').each(function() {
				members.push($( this ).attr('data-email'));
			});
            data1['group_members'] = members;
            data1['deadline'] = $('#meeting_deadlines option:selected').attr('data-id');
            data1['duration'] = $('#meeting_duration option:selected').attr('data-mins');
            data1['off_limits_start'] = $('#meeting_offlimits_start').val();
            data1['off_limits_end'] = $('#meeting_offlimits_end').val();
            //alert(JSON.stringify(data1) );
            $.ajax({
                type: 'POST',
                url: '/schedule',
                data: {'data': JSON.stringify(data1) },
                success: function(msg) {
                	//alert(msg);
                	times = $.parseJSON( msg );
                	//alert(times[0]);
                	times.map( function(time) {
	                    $('#meeting_times')
					        .append($("<option></option>")
					        .attr("data-datetime",time)
					        .text(time));
					});
					$('#meeting_times').selectpicker('refresh');
					
                },
                error: function(data, text) {
                    alert("Failed to schedule. Make sure everyone you want to schedule into the meeting has given access to their Google Calendars.");
                    $('#schedule-send-modal').modal('hide');
                }
            });
        });
    }
}


$( document ).ready( main );

