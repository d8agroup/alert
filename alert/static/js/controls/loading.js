(function( $ ){
    $.fn.ml_themes_loading = function(message) {

        //Embeded function to calculate css changes
        var calculate_css_values = function(container_height, container_width){

            if (container_height < 50 || container_width < 250)
                return {
                    'font-size': '18px',
                    'padding-top': parseInt(container_height / 3) + "px"
                };
            else if (container_height < 100 || container_width < 400)
                return {
                    'font-size': '25px',
                    'padding-top': parseInt(container_height / 3) + "px"
                };
            else
                return {
                    'font-size': '40px',
                    'padding-top': parseInt(container_height / 3) + "px"
                };
        };

        //Get a handle on the container
        var container = $(this);

        //Build the html
        var template = $('<div class="loading-message"><p><i class="icon-spinner icon-spin"></i> ' + message + '</p></div>');

        //Add some CSS
        var css_values = calculate_css_values(container.height(), container.width());
        for (var key in  css_values)
            template.find('p').css(key, css_values[key])

        //Add the template to the container
        container.html(template);

        //Return the container
        return container;
    };
})( jQuery );