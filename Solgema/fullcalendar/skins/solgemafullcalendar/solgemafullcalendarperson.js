//Ajax form to submit a person
jq('#form').submit(function(event) {
    event.preventDefault();

    var url = jq('#form').attr("action");
    var post_data = jq('#form').serialize() + '&form.buttons.save=Save'
    jq.post(url,post_data, function(data) {
        //When it is posted, we want to do a variety of things:
        //1) Remove the open timeslot on the calendar
        //2) Check for an error
        //3) Give a thank you if successful

        //1) Hiding the Green Element on the calendar
        var index = jq("#form").attr("action").indexOf('/++add++collective');
        var suburl = jq("#form").attr("action").substr(0,index);
        poster = 'a[href*="' + suburl + '"]';
        jq(poster).parent().hide()

        //2) Check for an ErrorCreating an ok box

        //3) Give a thank you if succssful
        jq('#event_edit_container').html('Thanks for "Leading the Way"! It means a lot not only to you, but also to the community. Looking forward to seeing you.');

        var ok = jq('<button>Ok</button>');

        jq('#event_edit_container').append(ok);
        ok.click(function(event) {
            //jq("#event_edit_container").parent().hide()
            //jq(".ui-widget-overlay").hide()
            window.parent.jq("#event_edit_container").dialog("close");
        })


    });

})


//return "Eek! A slight mishap seems to have taken place. We sincerely apologize for this faux pas, please feel free to contact us at leadtheway@ucsd.edu";
