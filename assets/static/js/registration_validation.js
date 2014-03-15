/**
 * @file pw_confirm.js
 * @author Joseph Ciurej
 * @date Spring 2014
 *
 * Validation Script for User Password Information
 *
 * @TODO
 * - Update the functionality of this script to inform the user of any failures
 *   in a more elegant fashion.
 */

/**
 * Main function for the 'pw_confirm.js' script file.
 */
function main()
{
	$( "form" ).on( "submit", function() {
		var password = $( "input[name=user_password]" ).val();
		var password_confirmation = $( "input[name=user_password_confirm]" ).val();

		if( password !== password_confirmation )
		{
			alert( "Password and password confirmation do not match!" );
			return false;
		}

		return true;
	} );
}


$( document ).ready( main );
