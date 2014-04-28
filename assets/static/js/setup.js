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
		$( ".timepicker-form" ).datetimepicker();

		// Setup the Select Modules //
		$( "select" ).selectpicker();
	}

	// Bind AJAX Requests to Fields //
	{
		// Setup the Google Authentication Button //
		$( "#google_auth" ).click( function() {
			$.post("google-auth-request", function(url) {
				window.location.replace(url);
			});
		} );

		// Setup the Group Page Buttons //
		$( "#leave_group" ).click( function() {
			var groupid = getGroupID();
			alert( "Leaving group #" + groupid + "!" );
			$.post( "/" );
		} );

		$( "#delete_group" ).click( function() {
			alert( "Deleting group" );
			$.post( "/" );
		} );

		$( "#add-member-submit" ).click( function() {
		} );

		// Setup Group Page Modal Submission Buttons //

		// TODO: Add group page submission button post requests.
	}
}


$( document ).ready( main );

