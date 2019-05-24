
        $(document).ready(function () {

            $('.select_nationality_class').bind('change', function () {
            var updated_na_value = $(this).val()
            var updated_na_value_id = $(this).attr('id')
            $(`#verified_nationality_${updated_na_value_id}`).val(updated_na_value)

        });


            $("#post_all").click(function (e) {
                e.preventDefault();
                var nationality_id = $(".nationality_pk_cls")
                let id_length = $(".nationality_pk_cls").length
                let score = $(".best_score")
                let input_score = $("#input_score").val()
                function compare(nationality_id, id_length, score, input_score) {
                    score_list = []
                    for (var i = 0; i < id_length; i++) {
                        if (score[i].value >= input_score) {
                            let score_val = $(score[i]).val()
                            let verified_nationality = $(score[i]).next().val()
                            var nationality_pk = $(score[i]).prev().val()
                            score_list.push({id: nationality_pk, score: score_val, Nationality: verified_nationality});
                        }
                    }
                    return score_list
                };
                compare(nationality_id, id_length, score, input_score)
                let csrftoken = $("[name=csrfmiddlewaretoken]").val();
                let url= $("#post_all").data("ajax-target");

        $.ajax({
            type:'POST',
            url:url,
            headers:{
              "X-CSRFToken": csrftoken
                },
            data: { 'best_score_list' : JSON.stringify(score_list), 'csrfmiddlewaretoken': csrftoken  },
             success: function(result) { //we got the response
             alert('Nationality having score greater than ' +input_score +' successfully updated.');
             window.location.reload(true);
         },
            error: function( status, exception) {
             alert('Cannot Update score greater than ' +input_score, exception);
             window.location.reload(true);
         }
        });
        return false;
    });
   });
