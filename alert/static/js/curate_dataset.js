(function( $ ){

    /******************************************************************************************************************/
    /* Static Functions */
    $.ml_alert_curate_dataset = {};

    $.ml_alert_curate_dataset.backwards = function() {

        //Set the new search data as the previous one
        $.ml_alert_curate_dataset.search_data($('#dataset-curate').data('previous_search_data'));

        //Repaint
        $.ml_alert_curate_dataset.repaint();
    };

    $.ml_alert_curate_dataset.repaint = function() {

        //Close the tag modal if open
        $('#tag-focus-modal').dialog('close');

        //Call the repaint instance method
        $('#dataset-curate').ml_alert_curate_dataset('repaint');
    };

    $.ml_alert_curate_dataset.search_data = function(search_data) {

        //Default search data
        var default_search_data = {
            sources: [],
            selected_tags: [],
            excluded_tags: []
        };

        //Get a handle on the container
        var container = $('#dataset-curate');

        //Check to see if this is the first call, if it is then add the default
        if (container.data('search_data') == null)
            container.data('search_data', default_search_data);

        //Check to see if this is the first call, if it is then add the default to the previous
        if (container.data('previous_search_data') == null)
            container.data('previous_search_data', default_search_data);

        //If search data is passed in then set it
        if (search_data != null) {

            //Clone the data into the previous
            container.data('previous_search_data', clone(container.data('search_data')));

            //Add the new search data
            container.data('search_data', search_data);
        }

        //Return the current search data
        return clone(container.data('search_data'));
    };

    $.ml_alert_curate_dataset.add_source_to_search_data = function(source) {

        //Get the current search data
        var search_data = $.ml_alert_curate_dataset.search_data();

        //Flag to see if the source is there already
        var found_in_collection = false;

        //Loop through the sources to see if this one is there
        $.each(search_data.sources, function(index, item){

            //If we already have it continue
            if (found_in_collection)
                return;

            //If this is not the one then continue
            if (item.guid != source.guid)
                return;

            //Set the active flag
            item.active = true;

            //Say we found it!
            found_in_collection = true;
        });

        //If it was not there then add it
        if (!found_in_collection) {

            //Set it as active
            source.active = true;

            //Add it to the collection
            search_data.sources[search_data.sources.length] = source;
        }

        //Save the collection back to data
        $.ml_alert_curate_dataset.search_data(search_data);
    };

    $.ml_alert_curate_dataset.add_tag_to_included_tags = function(tag){

        //First remove from exclude list
        $.ml_alert_curate_dataset.remove_tag_from_excluded_tags(tag);

        //Get the current search data
        var search_data = $.ml_alert_curate_dataset.search_data();

        //Flag to see if the tag is there already
        var found_in_collection = false;

        //Loop through the tags to see if this one is there
        $.each(search_data.selected_tags, function(index, item){

            //If we already have it continue
            if (found_in_collection)
                return;

            //If this is not the one then continue
            if (item != tag)
                return;

            //Say we found it!
            found_in_collection = true;
        });

        //If it was not there then add it
        if (!found_in_collection) {

            //Add it to the collection
            search_data.selected_tags[search_data.selected_tags.length] = tag;
        }

        //Save the collection back to data
        $.ml_alert_curate_dataset.search_data(search_data);
    };
    
    $.ml_alert_curate_dataset.remove_tag_from_included_tags = function(tag) {
        
        //Get the current search data
        var search_data = $.ml_alert_curate_dataset.search_data();

        //Create a new array for the edited tag list
        var new_selected_tags = []
        
        //Loop through the tags to see if this one is there
        $.each(search_data.selected_tags, function(index, item){

            //If this is the one then continue
            if (item == tag)
                return;

            //Add it to the new list
            new_selected_tags[new_selected_tags.length] = item;
        });

        //Add the new tags to the search data
        search_data.selected_tags = new_selected_tags;

        //Save the collection back to data
        $.ml_alert_curate_dataset.search_data(search_data);
    };

    $.ml_alert_curate_dataset.add_tag_to_excluded_tags = function(tag){

        //Also remove from selected list
        $.ml_alert_curate_dataset.remove_tag_from_included_tags(tag);

        //Get the current search data
        var search_data = $.ml_alert_curate_dataset.search_data();

        //Flag to see if the tag is there already
        var found_in_collection = false;

        //Loop through the tags to see if this one is there
        $.each(search_data.excluded_tags, function(index, item){

            //If we already have it continue
            if (found_in_collection)
                return;

            //If this is not the one then continue
            if (item != tag)
                return;

            //Say we found it!
            found_in_collection = true;
        });

        //If it was not there then add it
        if (!found_in_collection) {

            //Add it to the collection
            search_data.excluded_tags[search_data.excluded_tags.length] = tag;
        }

        //Save the collection back to data
        $.ml_alert_curate_dataset.search_data(search_data);
    };
    
    $.ml_alert_curate_dataset.remove_tag_from_excluded_tags = function(tag) {
        
        //Get the current search data
        var search_data = $.ml_alert_curate_dataset.search_data();

        //Create a new array for the edited tag list
        var new_excluded_tags = []
        
        //Loop through the tags to see if this one is there
        $.each(search_data.excluded_tags, function(index, item){

            //If this is the one then continue
            if (item == tag)
                return;

            //Add it to the new list
            new_excluded_tags[new_excluded_tags.length] = item;
        });

        //Add the new tags to the search data
        search_data.excluded_tags = new_excluded_tags;

        //Save the collection back to data
        $.ml_alert_curate_dataset.search_data(search_data);
    };

    $.ml_alert_curate_dataset.open_tag_focus_modal = function(tag){

        $('#tag-focus-modal').ml_themes_tag_focus_modal('open', tag);
    };

    $.ml_alert_curate_dataset.record_history = function(){

        //Get the history url
        var url = $('#dataset-curate').data('history_url');

        //Get a handle on the graph container
        var graph_container = $('#graph-main');

        //build the post data
        var post_data = {
            search_data: JSON.stringify($.ml_alert_curate_dataset.search_data()),
            svg: graph_container.html(),
            height: graph_container.height(),
            width: graph_container.width()
        };

        //Make the history request
        //TODO: handle the response template
        $.post(url, post_data, function(return_data){

            $('#dataset-curate').data('history_record_id', return_data.history_record_id)
        }, 'JSON');

    };

    /******************************************************************************************************************/
    /* Instance Functions */
    var methods = {
        init : function() {

            //get a handel on the container
            var container = this;

            //Attach the event handlers
            container.ml_alert_curate_dataset('attach_event_handlers');

            //return the container
            return container;
        },
        init_with_dataset: function(dataset){

            //get a handel on the container
            var container = this;

            //Add all the sources to the search data
            $.each(dataset.sources, function(index, item){
                $.ml_alert_curate_dataset.add_source_to_search_data(item);
            });

            //Repaint everything
            container.ml_alert_curate_dataset('repaint');

            //return the container
            return container;
        },
        init_with_history_record: function(history_record){

            //get a handel on the container
            var container = this;

            $.ml_alert_curate_dataset.search_data(history_record.search_data);

            //Repaint everything
            container.ml_alert_curate_dataset('repaint');

            //return the container
            return container;
        },
        set_display_css: function() {

            //get a handel on the container
            var container = this;

            //Set the height of the graph area
            container.find('#curation-list').height($(window).height() - 100 - $('#curation-filters').height());
            container.find('.content-item').each(function(index, item){

                var content_item = $(item);
                var content_item_actions = content_item.find('.content-item-actions');

                var content_data_height = content_item.find('.content-item-data').height();
                var content_actions_height = content_item_actions.height();
                if (content_data_height > content_actions_height)
                    content_item_actions.height(content_data_height);

                var curation_buttons = content_item.find('.content-item-curation-buttons');
                curation_buttons.css('margin-top', parseInt((content_item_actions.height() - curation_buttons.height()) / 2) + "px")
            });

            //return the container
            return container;
        },
        repaint: function() {

            //get a handel on the container
            var container = this;

            //Show loading
            container.find('#curation-filters').ml_alert_loading('Loading filters');
            container.find('#curation-list').ml_alert_loading('Loading content');

            //Build the post data for the api call
            var post_data = {
                csrfmiddlewaretoken: $.cookie('csrftoken'),
                search_data: JSON.stringify($.ml_alert_curate_dataset.search_data())
            };

            //Get the repaint url
            var url = container.find('#search-url').val();

            //Make the api call
            $.post(url, post_data, function(return_data){

                //Check the status
                if (return_data.status == 'ok') {

                    $('#curation-list').html(return_data.content_template);

                    //Wait a couple of seconds then record the history step
//                    setTimeout(function(){
//                        $.ml_alert_curate_dataset.record_history();
//                    }, 4500);
                }
                else {

                    alert('error');
//                    //Get a handel on the gaph container
//                    var graph_container = $('#graph-main');
//
//                    //Build the template
//                    var template = $('' +
//                        '<div class="state-error">' +
//                            '<h5>Sorry something went wrong</h5>' +
//                            '<p><i class="icon-warning-sign"></i> There was an error rendering that graph, it could be ' +
//                            'that there is nothing that matches your current filters, please use the back button below:' +
//                            '</p>' +
//                            '<p>' +
//                                '<a class="btn" id="back-button"><i class="icon-backwards"></i> back</a>' +
//                            '</p>' +
//                        '</div>');
//
//                    //Find and attach to the backwards button
//                    template.find('#back-button').click(function(){
//                        $.ml_alert_curate_dataset.backwards();
//                    });
//
//                    //Set the margin of the template
//                    template.css('margin-top', parseInt(graph_container.height() / 3) + "px");
//
//                    //Put things in error state
//                    graph_container.html(template);
                }

                //Set the display css
                container.ml_alert_curate_dataset('set_display_css');
            });

            //return the container
            return container;

        },
        attach_event_handlers: function(){

            //get a handel on the container
            var container = this;

            //Attach to the window resize event
            $(window).resize(function(){
                $('#dataset-curate').ml_alert_curate_dataset('set_display_css');
            });

            //return the container
            return container;
        }
    };

    /******************************************************************************************************************/
    /* Instance Method Locator */
    $.fn.ml_alert_curate_dataset = function( method ) {
        if ( methods[method] ) { return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));}
        else if ( typeof method === 'object' || ! method ) { return methods.init.apply( this, arguments ); }
        else { $.error( 'Method ' +  method + ' does not exist on jQuery.django_odc_dataset_explore' ); }
    };

})( jQuery );