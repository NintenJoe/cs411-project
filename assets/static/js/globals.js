/**
 * @file globals.js
 * @author Joseph Ciurej
 * @date Spring 2014
 *
 * Module for all Globally Accessible Javascript Functions
 *
 * @TODO
 * - Write the implementation for this script!
 */

/**
 * The validation function for all basic fields using bootstrap editable.
 *
 * @see http://vitalets.github.io/x-editable/demo-bs3.html
 */
function validateFieldForm( _value )
{
	if( $.trim(_value) == "" )
		return "Field Required";
}


function addEditableToForms( _id )
{
	$.fn.editable.defaults.mode = "popup";
	$( _id + " .editable-field" ).editable( { placement: "bottom", validate: validateFieldForm } );
	$( _id + " .editable-date" ).editable( { placement: "bottom", firstitem: "name" } );
	$( _id + " .editable-notes" ).editable( { placement: "right", validate: validateFieldForm } );
}


function bindAsyncToDeadlines( _id )
{
	$( _id + " .deadline-remove-icon" ).click( function() {
		// TODO: Move to on success.
		var deadlineID = $( this ).data( "id" );
		$( "#deadline-" + deadlineID ).remove();

		// TODO: Add functionality to remove this deadline from the DB.
		// TODO: Add asynchronous functionality here.
	} );
	
	$( _id + " .deadline-notes" ).hide();
	$( _id + " .deadline-expand-icon" ).click( function() {
		var deadlineID = $( this ).data( "id" );
		$( "#deadline-" + deadlineID ).find( ".deadline-notes" ).slideToggle( "slow" );
	} );
}

