$(document).ready(function() {
  $('table.index tr:odd').addClass('odd');
  $('a.delete').click(function(e) {
    var href = $(this).attr('href'),
        method = 'delete',
        form = $('<form method="post" action="'+href+'"></form>'),
        metadata_input = '<input name="_method" value="'+method+'" type="hidden" />';
    form.hide().append(metadata_input).appendTo('body');
    e.preventDefault();
    form.submit();
  })
  
  $('.datepicker').datepicker({
    dateFormat: 'yy-mm-dd'
  })
})