$(function() {

    $('#account-settings-form-link').click(function(e) {
		$("#account-settings-form").delay(100).fadeIn(100);
 		$("#reset-password-form").fadeOut(100);
		$('#reset-password-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#reset-password-form-link').click(function(e) {
		$("#reset-password-form").delay(100).fadeIn(100);
 		$("#account-settings-form").fadeOut(100);
		$('#account-settings-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});

});