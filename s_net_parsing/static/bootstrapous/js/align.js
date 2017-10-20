;(function($){
        $.extend($.fn,{
            // Overlay ; $(body).overlay();
            overlay: function(o){

                var d={
                addClass:'',
                css:{},
                opacity:0.5,
                autoOpen:true,
                zIndex:1000,
                onOpen:function(){x.show();},
                onClose:function(){x.hide();},
                onRemove:function(){x.remove();}
            },x,l;

            // Merge Options
            o=$.extend({},d,o);


            // Create overlay element
            x=$('<div>',{css:{opacity:o.opacity,zIndex:o.zIndex}}).css(o.css).addClass('overlay '+o.addClass).hide().appendTo(this);

            // If appended to body element, set position fixed
            this[0].tagName.toLowerCase()=="body"&&x.css("position","fixed");

            // Overlay Control Object
            l = {
                remove:function(){o.onRemove(l)},
                open:function(){o.onOpen(l)},
                close:function(){o.onClose(l)},
                obj:x
            };

            // Call On Show
            o.autoOpen&& o.onOpen(l);

            // Return Object
            return l;
        },


        align:function(o){

            var d={
                x:'center',
                y:'center',
                position:'fixed',
                parent:window
            };

            o=$.extend({},d,o);

            var c=$(o.parent),
                t=$(this),
                s=c.scrollTop(),
                top,
                left;

            t.css('position',o.position); // Set Css Position

            if(o.y)top  = o.y=='center' ? (c.height()/2) - (t.innerHeight()/2) : o.y;
            if(o.x)left = o.x=='center' ? (c.width()/2) - (t.innerWidth()/2) : o.x;
            if(o.position=='absolute') top += s; // For absolute position
            if(top<0) top=0;

            t.css({top:top,left:left});
        },

    });

})(jQuery);