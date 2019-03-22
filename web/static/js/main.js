
$(function(){
    //TODO: get allowed times dinamically from settings.
    $(".dateTimePicker").datetimepicker({
        format:'Y-m-d H:i',
        allowTimes:[
          '12:00', '12:30',
          '13:00', '13:30',
          '14:00', '14:30',
          '19:00', '19:30',
          '20:00', '20:30',
          '21:00', '21:30',
          '22:00'
         ]
    });

    $(".confirm").on('click', function () {
        return confirm('Are you sure?');
    });
});
