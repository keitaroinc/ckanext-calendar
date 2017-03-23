$(document).ready(function () {

  var datePickerElements = $('.date-picker');

  datePickerElements.each(function (e) {
    var calendarSelector = $("#" + $(this).attr('id'));
    var calendarInput = "#" + $(this).attr('id') + "-input";
    var calendarOptions = {
      showButtonPanel: true,
      dateFormat: "yy-mm-dd 00:00:00",
      altField: calendarInput
    };
    calendarSelector.datepicker(calendarOptions);
  });

});