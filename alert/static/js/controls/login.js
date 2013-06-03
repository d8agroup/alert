(function( $ ){

    /******************************************************************************************************************/
    /* Instance Functions */
    var methods = {
        init : function() {

            //get a handel on the container
            var container = this;

            //Call the attach event handlers
            container.ml_themes_login('attach_event_handlers');

            //return the container
            return container;
        },
        attach_event_handlers: function(){

            //get a handel on the container
            var container = this;

            //Find the login button
            var button = container.find('button');

            //Attach to the click event
            button.click(function(e){

                //Prevent defaults
                e.preventDefault();

                //Get a handle on the button
                var button = $(this);

                //get a handel on the form
                var form = button.parents('form:first');

                //Get the post url
                var url = form.attr('action');

                //Get the post data
                var post_data = form.serialize();

                //Disable the button and show the spinner
                button
                    .addClass('disabled')
                    .find('i').attr('class', 'icon-spinner icon-spin');

                //Make the api request
                $.post(url, post_data, function(return_data){

                    //if there was an error show the new template
                    if (return_data.status == 'error') {

                        //Add the template
                        container.html(return_data.template);

                        //Attach to the event handlers again
                        container.ml_themes_login('attach_event_handlers');
                    }

                    //if its a pass then follow the redirect
                    if (return_data.status == 'ok')
                        document.location.href = return_data.redirect;
                });
            });

            //return the container
            return container;
        }
    };

    /******************************************************************************************************************/
    /* Instance Method Locator */
    $.fn.ml_themes_login = function( method ) {
        if ( methods[method] ) { return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));}
        else if ( typeof method === 'object' || ! method ) { return methods.init.apply( this, arguments ); }
        else { $.error( 'Method ' +  method + ' does not exist on jQuery.django_odc_login' ); }
    };

})( jQuery );