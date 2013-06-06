(function( $ ){

    /******************************************************************************************************************/
    /* Instance Functions */
    var methods = {
        init : function() {

            //get a handel on the container
            var container = this;

            //Apply loading
            container.find('#admin-users-summary-content').ml_alert_loading('Loading Users');

            //Call the attach event handlers
            container.ml_alert_admin_users_summary('reload_users');

            //return the container
            return container;
        },
        reload_users: function(){

            //get a handel on the container
            var container = this;

            $.get(url('admin_users_summary'), function(template){

                var users_summary_container = container.find('#admin-users-summary-content');

                users_summary_container.html(template);
            });

            //return the container
            return container;
        }
    };

    /******************************************************************************************************************/
    /* Instance Method Locator */
    $.fn.ml_alert_admin_users_summary = function( method ) {
        if ( methods[method] ) { return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));}
        else if ( typeof method === 'object' || ! method ) { return methods.init.apply( this, arguments ); }
        else { $.error( 'Method ' +  method + ' does not exist on jQuery.ml_alert_admin_users_summary' ); }
    };

})( jQuery );