var scrolltotop={setting:{startline:1,scrollto:0,scrollduration:200,fadeduration:[300,100]},controlHTML:"",controlattrs:{offsety:50},anchorkeyword:"#top",state:{isvisible:false,shouldvisible:false},scrollup:function(){if(!this.cssfixedsupport){this.$control.css({opacity:0})}var a=isNaN(this.setting.scrollto)?this.setting.scrollto:parseInt(this.setting.scrollto);if(typeof a=="string"&&jQuery("#"+a).length==1){a=jQuery("#"+a).offset().top}else{a=0}this.$body.animate({scrollTop:a},this.setting.scrollduration)},keepfixed:function(){var c=jQuery(window);var b=c.scrollLeft()+c.width()-this.$control.width();var a=c.scrollTop()+c.height()-this.$control.height()-this.controlattrs.offsety;this.$control.css({left:"50%",top:a+"px"})},togglecontrol:function(){var a=jQuery(window).scrollTop();if(!this.cssfixedsupport){this.keepfixed()}this.state.shouldvisible=(a>=this.setting.startline)?true:false;if(this.state.shouldvisible&&!this.state.isvisible){this.$control.stop().animate({opacity:1},this.setting.fadeduration[0]);this.state.isvisible=true}else{if(this.state.shouldvisible==false&&this.state.isvisible){this.$control.stop().animate({opacity:0},this.setting.fadeduration[1]);this.state.isvisible=false}}},init:function(){jQuery(document).ready(function(c){var a=scrolltotop;var b=document.all;a.cssfixedsupport=!b||b&&document.compatMode=="CSS1Compat"&&window.XMLHttpRequest;a.$body=(window.opera)?(document.compatMode=="CSS1Compat"?c("html"):c("body")):c("html,body");a.$control=c('<div id="tag_gotop">'+a.controlHTML+"</div>").appendTo("body");c("#tag_gotop").css({position:a.cssfixedsupport?"fixed":"absolute",bottom:a.controlattrs.offsety,right:a.controlattrs.offsetx,opacity:0,cursor:"pointer"});c("#tag_gotop").click(function(){a.scrollup();return false});if(document.all&&!window.XMLHttpRequest&&a.$control.text()!=""){a.$control.css({width:a.$control.width()})}a.togglecontrol();c('a[href="'+a.anchorkeyword+'"]').click(function(){a.scrollup();return false});c(window).bind("scroll resize",function(d){a.togglecontrol()});c(window).resize(function(){if(!a.cssfixedsupport){if(jQuery(window).width()<982){c("#tag_gotop").css({display:"none"})}else{c("#tag_gotop").css({display:"block"})}}})})}};scrolltotop.init();