$.Message = function(msg){
    var $t = $("#message");
    if(typeof msg == "string"){
        $t.text(msg).show();
        setTimeout(function(){
            $t.fadeOut(500);
        }, 3000);  
    }
};

$.fn.navLink = function(){
    var $t = $(this);
    $t.find("li").each(function(){
        $(this).find("a").click(function(){
            $t.find("a.active").removeClass("active");
            $(this).addClass("active");
        });
    });
};

$.fn.formStep = function(){
    var $li = $(this).find("li");        
    var hideTimer=400, showTimer=200;
    
    $li.first().find("#prev_button").remove();
    $li.last().find("#next_button").remove();
    
    $li.each(function(i, t){
        if(i > 0) $(t).hide();
        $(t).find(".prev_button").click(function(){
            $(t).fadeOut(hideTimer, function(){
                $(t).prev("li").fadeIn(showTimer);
            });
        });
        $(t).find(".next_button").click(function(){
            $(t).fadeOut(hideTimer, function(){
                $(t).next("li").fadeIn(showTimer);
            });
        });
    });
};

$.fn.doRemove = function(){    
    $(this).each(function(){
        var $t = $(this);
        $t.click(function(){
        if(confirm("确定要执行删除吗？")){
            var url = $t.attr("href");                                               
            url += url.indexOf("?") == -1 ? "?" : "&";
                       
            $.ajax({
                type:'GET',
                url:url+"t="+Math.random(),
                data:{},
                success:function(r){
                    r = r.toString();
                    if(r == 'success'){                                                
                        $t.parents("tr").fadeOut(500);
                        $.Message("删除成功。");                                                                                          
                    } else {
                        $.Message("删除失败。");
                    }
                }
            });                        
        }
        
        return false;   
        });
    });
};

$.fn.tab = function(){
    var $this = $(this).children();
    var $box = $("#" + $(this).attr("boxid"));
    $box.children(":gt(0)").hide();
    $this.each(function(){        
        var index = $(this).index();   
        $(this).find("a").click(function(){           
            $this.find("a").removeClass("active");
            $(this).addClass("active");
            $box.children().hide();            
            $($box.children().get(index)).show();           
        });
    });
};

$.fn.choseAll = function(){
    $(this).click(function(){
        if($(this).attr("checked").toString() == 'true') {
            $(".pcode").attr("checked", true);
        } else {
            $(".pcode").attr("checked", false);
        }
        return true;        
    });    
};

$(document).ready(function(){    
    $("#mainNav").navLink();   
});