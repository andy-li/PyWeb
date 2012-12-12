(function(wi, sk){
    sk = wi[sk];
    sk.add(sk.global, {
        lazy: function(option){
            var settings = {
                obj: null,
                defHeight: -200
            };
            settings = $.extend(settings, option || {});
            var defHeight = settings.defHeight, obj = (typeof settings.obj == "object") ? settings.obj.find("img") : $(settings.obj).find("img");
            var pageTop = function(){
                return document.documentElement.clientHeight + Math.max(document.documentElement.scrollTop, document.body.scrollTop) - settings.defHeight
            };
            var imgLoad = function(){
                obj.each(function(){
                    if ($(this).offset().top <= pageTop()) {
                        var original = $(this).attr("original");
                        if (original) {
                            $(this).attr("src", original).removeAttr("original").hide().fadeIn();
                        }
                    }
                })
            };
            imgLoad();
            $(window).bind("scroll", function(){
                imgLoad()
            })
        }
    });
    
    sk.ready(function(){
        sk.global.lazy({obj : "#container"});
    });
	    
})(this, 'SKD');
