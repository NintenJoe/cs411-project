/**
 * @file edit_validation.js
 * @author Joseph Ciurej
 * @date Spring 2014
 *
 * Validates Input for the "Edit" User Page
 *
 * @TODO
 */

/**
 * Main function for the 'edit_validation.js' script file.
 */
function main()
{
	// TODO: Refactor this code... there's a lot of duplication here.
	$( "input[name=add_group]" ).click( function() {
		var added_group = $( "select[name=available_groups] :selected" );
		var added_group_name = added_group.text();
		var new_group_element = $( "<option> </option>" )
			.attr( "value", added_group_name )
			.text( added_group_name ); 

		$( "select[name=user_groups]" ).append( new_group_element );
		added_group.remove();
	} );
	$( "input[name=rem_group]" ).click( function() {
		var removed_group = $( "select[name=user_groups] :selected" );
		var removed_group_name = removed_group.text();
		var new_group_element = $( "<option> </option>" )
			.attr( "value", removed_group_name )
			.text( removed_group_name ); 

		$( "select[name=available_groups]" ).append( new_group_element );
		removed_group.remove();
		
	} );

	$( "form" ).on( "submit", function() {
		// Validate password information.
		var password = $( "input[name=user_password]" ).val();
		var password_confirmation = $( "input[name=user_password_confirm]" ).val();

		if( password !== password_confirmation )
		{
			alert( "Password and password confirmation do not match!" );
			return false;
		}

		// Parse user group information.
		var new_group_string = "";
		$( "select[name=user_groups] option" ).each( function()
		{
			new_group_string += $( this ).val() + "~";
		} );
		new_group_string = new_group_string !== "" ? new_group_string.slice( 0, -1 ) : "";
		$( "input[name=new_user_groups]" ).val( new_group_string );

		return true;
	} );
}


$( document ).ready( main );
