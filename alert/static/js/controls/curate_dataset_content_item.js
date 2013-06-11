(function( $ ){

    /******************************************************************************************************************/
    /* Static Functions */
    $.ml_alert_curate_dataset_content_item = {};

    /******************************************************************************************************************/
    /* Instance Functions */
    var methods = {
        init : function() {

            //get a handel on the container
            var container = this;

            //Check if this item has been inited
            if (!container.is('.active-content-item')) {

                //Say it has been inited
                container.addClass('active-content-item');

                //Attach the event handlers
                container.ml_alert_curate_dataset_content_item('attach_event_handlers');
            }

            //return the container
            return container;
        },
        attach_event_handlers: function(){

            //get a handel on the container
            var container = this;

            //Attach to the mouse over
            container.mouseover(function(){
                $(this).addClass('mousedover');
            });

            //Attach to the curation buttons
            container.find('.content-item-curation-buttons a').click(function(){

                //Get a handle on the clicked button
                var button = $(this);

                //get a handle on the container
                var container = button.parents('.content-item:first');

                //Get the content item data
                var content_item = container.data('content_item');

                //get the curation direction
                var curation_direction = button.data('curation_direction');

                //Get a list of all the current content items
                var content_item_ids = [];
                $('.content-item').each(function(index, item){
                    content_item_ids.push($(item).data('content_item').id);
                });

                //Build the post data for the api
                var post_data = {
                    csrfmiddlewaretoken: $.cookie('csrftoken'),
                    search_data: JSON.stringify($.ml_alert_curate_dataset.search_data()),
                    content_item: JSON.stringify(content_item),
                    curation_direction: curation_direction,
                    content_item_ids: JSON.stringify(content_item_ids)
                };

                //If there was an actual user click then animate else just remove
                if (button.is('.curation-button-ignore'))
                    container.remove();
                else
                    container.slideUp(function(){$(this).remove()});

                $.ml_alert_curate_dataset.refresh_content_list(post_data);
            });

            //return the container
            return container;
        }
    };

    /******************************************************************************************************************/
    /* Instance Method Locator */
    $.fn.ml_alert_curate_dataset_content_item = function( method ) {
        if ( methods[method] ) { return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));}
        else if ( typeof method === 'object' || ! method ) { return methods.init.apply( this, arguments ); }
        else { $.error( 'Method ' +  method + ' does not exist on jQuery.django_odc_dataset_explore' ); }
    };

})( jQuery );