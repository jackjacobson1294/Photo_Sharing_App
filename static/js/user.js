$('#new_submit').click( function(e) {
	e.preventDefault();
	$.ajax({
		type: 'POST',
		contentType: "application/json; charset=UTF-8",
		data: JSON.stringify({'username': $("#new_username_input").val(),
				'firstname': $("#new_firstname_input").val(),
				'lastname': $("#new_lastname_input").val(),
				'password1': $("#new_password1_input").val(),
				'password2': $("#new_password2_input").val(),
				'email': $("#new_email_input").val()}),
		url: 'http://localhost:3000/p2gkisj6/p3/api/v1/user',
		success: function(data) {
			return alert(data);
		},
		error: function(error) {
			console.log("failure");
		}
	});
});