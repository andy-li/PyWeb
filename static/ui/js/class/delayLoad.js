(function(wi, sk){
	sk = wi[sk];
	sk.add(sk.global, {
		delayLoad : function(option) {
			var options = {
                obj: null,
                fn: null
            };
            
            options = $.extend(options, option || {});
            var obj = (typeof options.obj == "object") ? options.obj : $(options.obj);
            
            var load = function(){
                obj.find("img").each(function(){
                    var org = $(this).attr("original");
                    if (org) {
                        $(this).attr("src", org).removeAttr("original").hide().fadeIn();
                    }
                });
            };
            
            var init = function(){
                var S = [load];
                
                if (sk.global.notEmptyArray(options.fn)) {
                    $.each(options.fn, function(i, n){
                        if (typeof n == 'function') {
                            S.push(n);
                        }
                    });
                }
                else 
                    if (typeof options.fn == 'function') {
                        S.push(options.fn);
                    }
                
                sk.global.queue(obj, S);
            };
            
            init();
		}
	});
	
    sk.ready(function(){
		sk.loader.require('class.masonry', function() {
            if ($('#ppbox')[0]) {
                sk.global.delayLoad({
                    obj: '#ppbox',
                    fn: function(){
                        var $p = $('#ppbox');
                        $p.imagesLoaded(function(){
                            $p.masonry({
                                itemSelector: 'dl'
                            });
                        });
                        $p.find('dl').hover(function(){
                            $(this).find('a.love').show();
                            $(this).addClass('hover_bg');
                        }, function(){
                            $(this).find('a.love').hide();
                            $(this).removeClass('hover_bg');
                        });
                    }
                });
            }		
		});		        
    });
	
})(this, 'SKD');
