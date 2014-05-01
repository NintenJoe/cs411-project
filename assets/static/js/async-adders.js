/**
 * @file async-adders.js
 * @author Joseph Ciurej
 * @date Spring 2014
 *
 * Module File Containing all Asynchronous Adding Functions
 *
 * @TODO
 * - Write the implementation for this script!
 */

/// Formation Handling Functions ///

/**
 * @return entryHTML The HTML associated with a user entry with the given attributes.
 */
function formUserEntry( _name, _email, _iconURL )
{
	var entry = "";
	entry += '<li style="list-style-image: url(' + _iconURL + ');">';
	entry += '  <h4 class="inner-heading pull-left">';
	entry += '    ' + _name + ' <small>' + _email + '</small>';
	entry += '  </h4>';
	entry += '</li>';

	return entry;
}


/**
 * @return entryHTML The HTML associated with a user group with the given attributes.
 */
function formGroupEntry( _id, _name, _maintainer )
{
	var entry = "";
	entry += '<ul class="group-forest">';
	entry += '  <li>';
	entry += '    <a href="/group/' + _id + '">';
	entry += '      <h5 class="inner-heading">';
	entry += '        ' + _name;
  if (undefined !== _maintainer) {
	    entry += '        <small>' + _maintainer + '</small>';
  }
	entry += '      </h5>';
	entry += '    </a>';
	entry += '  </li>';
	entry += '</ul>';

	return entry;
}


function formDeadlineEntry( _id, _name, _groupName, _type, _time, _notes, _editable )
{
	var entryName = '';
	var entryTime = '';
	var entryIcons = '';

	if( _editable )
	{
		entryName += '<a href="#" class="editable-field" data-name="name" data-type="text" data-pk="' + _id + '" data-url="/update-deadline-name" data-title="Enter New Name">';
		entryName += '  ' + _name;
		entryName += '</a>';

		entryTime += '<a href="#" class="editable-date" data-viewformat="dddd MMMM DD, HH:mm A" data-format="YYYY-MM-DD HH:mm" data-template="MMMM DD, HH:mm" data-type="combodate" data-pk="' + _id + '" data-url="/update-deadline-time" data-title="Enter New Time">';
		entryTime += '  ' + _time;
		entryTime += '</a>';

		entryIcons += '<div class="deadline-icon-group pull-right">'
		entryIcons += '  <span data-id="' + _id + '" class="glyphicon glyphicon-remove deadline-icon deadline-remove-icon"></span>';
		entryIcons += '  <span data-id="' + _id + '" class="glyphicon glyphicon-chevron-down deadline-icon deadline-expand-icon"></span>';
		entryIcons += '</div>';
	}
	else
	{
		entryName += _name;
		entryTime += _time;
		entryIcons += '<div class="deadline-icon-group pull-right">';
		entryIcons += '  <span data-id="' + _id + '" class="glyphicon glyphicon-chevron-down deadline-icon deadline-expand-icon"> </span>';
		entryIcons += '</div>'
	}

	var entry = "";
	entry += '<li id="deadline-' + _id + '" class="deadline-entry ' + _type + '">';
	entry += '  <h5 class="inner-heading">';
	entry += '    <strong>' + _groupName + ': </strong>' + entryName;
	entry += '    <small>' + entryTime + '</small>';
	entry += '  </h5>';
	entry += '  ' + entryIcons;
	entry += '  <ul class="deadline-notes">';
	entry += '    <li><small>';
	entry += '      <a href="#" class="editable-notes" data-name="notes" data-type="text" data-pk="' + _id + '" data-url="/update-deadline-notes" data-title="Enter New Notes">' + _notes + '</a>';
	entry += '    </small></li>';
	entry += '  </ul>';
	entry += '</li>';

	return entry;
}

/// Add Handling Functions ///

function addUserEntry( _name, _email, _iconURL )
{
	var entry = formUserEntry( _name, _email, _iconURL );
	$( entry ).appendTo( ".member-list" );
}


function addGroupEntry( _id, _name, _maintainerName )
{
	var entry = formGroupEntry( _id, _name, _maintainerName );
	$( entry ).appendTo( ".group-tree" );
}


function addDeadlineEntry( _id, _name, _groupName, _type, _time, _notes, _editable )
{
	var htmlID = "#deadline-" + _id;

	var entry = formDeadlineEntry( _id, _name, _groupName, _type, _time, _notes, _editable );
	$( entry ).appendTo( ".deadline-list" );

	bindAsyncToDeadlines( htmlID );
	addEditableToForms( htmlID );
}


