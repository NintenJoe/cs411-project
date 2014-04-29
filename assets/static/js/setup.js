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
		$( ".editable-field" ).editable();

		// Setup the Deadline List Modules //
		$( ".deadline-notes" ).hide();
		$( ".deadline-entry" ).click( function() {
			$( this ).find( ".deadline-notes" ).slideToggle( "slow" );
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
		var substringMatcher = function(strs) {
			return function findMatches(q, cb) {
			var matches, substringRegex;
			 
			// an array that will be populated with substring matches
			matches = [];
			 
			// regex used to determine if a string contains the substring `q`
			substrRegex = new RegExp(q, 'i');
			 
			// iterate through the pool of strings and for any string that
			// contains the substring `q`, add it to the `matches` array
			$.each(strs, function(i, str) {
			if (substrRegex.test(str)) {
			// the typeahead jQuery plugin expects suggestions to a
			// JavaScript object, refer to typeahead docs for more info
			matches.push({ value: str });
			}
			});
			 
			cb(matches);
			};
			};
			 
			var states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
			'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
			'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
			'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
			'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
			'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
			'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
			'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
			'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
			];

		$( "#new_user_email" ).typeahead( { hint: true, highlight: true, minlength: 2 },
			{ name: "states", displaykey: "value", source: substringMatcher(states) } );
		// TODO: Only allow this feature if the user can add courses.
		$( "#group_name" ).typeahead( { hint: true, highlight: true, minlength: 2 },
			{ name: "states", displaykey: "value", source: substringMatcher(states) } );
		$( "#deadline_name" ).typeahead( { hint: true, highlight: true, minlength: 2 },
			{ name: "states", displaykey: "value", source: substringMatcher(states) } );
	}

	// Bind AJAX Requests to Fields //
	{
		// Setup the Google Authentication Button //
		$( "#google_auth" ).click( function() {
			$.post("google-auth-request", function(url) {
				window.location.replace(url);
			});
		} );

        $( "#leave_group" ).click( function () {
            var data1 = {};
            data1['group_id'] = getGroupID();
            $.ajax({
                type: 'POST',
                url: '/leave-group',
                data: {'data': JSON.stringify(data1)},
                dataType: 'application/json',
                complete: function(msg) {
                    window.location.reload();
                },
                fail: function(data) {
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
                dataType: 'application/json',
                complete: function(msg) {
                    window.location.reload();
                },
                fail: function(data) {
                    alert("Failed to delete group.");
                }
            }); 
		});
        
        $( "#add-member-submit" ).click( function () {
            var data1 = {};
            data1['group_id'] = getGroupID();

            // Input element has no ID tag defined 
            data1['user_email'] = $('[name="user_email"]').val();
            $.ajax({
                type: 'POST',
                url: '/add-member',
                data: {'data': JSON.stringify(data1)},
                dataType: 'application/json',
                complete: function(msg) {
                    $('#add-member-modal').modal('hide');
                },
                fail: function(data) {
                    alert("Failed to add user to group.");
                }
            });
        });
            
                    
        $( "#add-subgroup-submit" ).click( function () {
            var data1 = {};
            data1['group_id'] = getGroupID();

            // Input element has no ID tag defined 
            data1['group_name'] = $('[name="group_name"]').val();
            data1['group_description'] = $('[name="group_description"]').val();
            $.ajax({
                type: 'POST',
                url: '/add-subgroup',
                data: {'data': JSON.stringify(data1)},
                dataType: 'application/json',
                complete: function(msg) {
                    $('#add-subgroup-modal').modal('hide');
                },
                fail: function(data) {
                    alert("Failed to add subgroup.");
                }
            });
        });
        

	    // Setup Group Page Modal Submission Buttons //

		// TODO: Add group page submission button post requests.
	}
}


$( document ).ready( main );

