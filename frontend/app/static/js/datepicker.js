/**
 * @author Damien LE BORGNE
 */

$(document).ready(function(){
    var dateByForkStart=$('input[name="dateByForkStart"]');
    var dateByForkEnd=$('input[name="dateByForkEnd"]');
    var date_input_year=$('input[name="dateByYear"]');
    var container=$('#sidebar');
    var currentDate = new Date();
    // mettre date min 2010


    dateByForkStart.datepicker({
        format: 'dd/mm/yyyy',
        container: container,
        todayHighlight: true,
        autoclose: true,
        endDate: "currentDate",
        maxDate: currentDate
      }).on('changeDate', function (ev) {
         $(this).datepicker('hide');
      });


    dateByForkEnd.datepicker({
        format: 'dd/mm/yyyy',
        container: container,
        todayHighlight: true,
        autoclose: true,
        endDate: "currentDate",
        maxDate: currentDate
      }).on('changeDate', function (ev) {
         $(this).datepicker('hide');
      });

    date_input_year.datepicker({
        format: 'yyyy',
        viewMode: "years", 
        minViewMode: "years",
        container: container,
        todayHighlight: true,
        autoclose: true,
        endDate: "currentDate",
        maxDate: currentDate
    }).on('changeDate', function (ev) {
        $(this).datepicker('hide');
     });
    

    $('input[type="radio"]').click(function(){
        var inputValue = $(this).attr("value");
        var targetBox = $("." + inputValue);
        $(".div").not(targetBox).hide();
        document.getElementById(inputValue).style.display = 'block';
        // Va si une autre maniere existe
        switch (inputValue){
            case 'tout':
                date_input_year.datepicker('setDate', null);
                dateByForkStart.datepicker('setDate', null);
                dateByForkEnd.datepicker('setDate', null);
                break; 
            case 'periode':
                date_input_year.datepicker('setDate', null);
                break;
            case 'annee':
                dateByForkStart.datepicker('setDate', null);
                dateByForkEnd.datepicker('setDate', null);
                break;
        }

    });

})
