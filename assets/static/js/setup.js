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

function getBloodhoundForURL( _url )
{
	var replacefun = function( u, q ) { return u + "?query=" + q; };

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
		$.fn.editable.defaults.mode = "popup";
		$( ".editable-field" ).editable( { placement: "bottom" } );
		$( ".editable-date" ).editable( { placement: "bottom", firstitem: "name" } );
		$( ".editable-notes" ).editable( { placement: "right" } );

		// Setup the Deadline List Modules //
		$( ".deadline-notes" ).hide();
		$( ".deadline-expand-icon" ).click( function() {
			var deadlineID = $( this ).data( "id" );
			$( "#deadline-" + deadlineID ).find( ".deadline-notes" ).slideToggle( "slow" );
		} );

		// Setup the Datetime Picker Modules //
		$( ".datetimepicker-form" ).datetimepicker();
		$( ".timepicker-form" ).datetimepicker( {pickDate: false} );

		// Setup the Select Modules //
		$( "select" ).selectpicker();
		// TODO: Select all members by default in schedule modal select.
	}

	// Set up Autocomplete Fields ///
	{
		var typeahead_options = { hint: true, highlight: true, minLength: 2 };

		$( "#new_user_email" ).typeahead( typeahead_options,
			{ name: "emails", displaykey: "value", 
			source: getBloodhoundForURL("../get-users").ttAdapter() } );
		$( "#group_name" ).typeahead( typeahead_options,
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
        $( "#leave_group" ).click( function () {
            var data1 = {};
            data1['group_id'] = getGroupID();
            $.ajax({
                type: 'POST',
                url: '/leave-group',
                data: {'data': JSON.stringify(data1)},
                success: function(msg) {
                    window.location.reload();
                },
                error: function(data) {
                    alert("Failed to leave group.");
                }
            });
        });
        
		$( "#delete_group" ).click( function() {
				var data1 = {};
				data1['group_id'] = getGroupID();
				
				$.ajax({
					type: 'POST',
					url: '/delete-group',
					data: {'data': JSON.stringify(data1)},
					success: function(msg) {
						window.location.reload();
					},
					error: function(data) {
						alert("Failed to delete group.");
					}
				}); 
		});
        
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
                    $('#add-member-modal').modal('hide');
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
                },
                error: function(data, text) {
                    alert("Failed to add subgroup." + text);
                }
            });
        });
    }
}


$( document ).ready( main );

