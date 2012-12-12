(function(wi, sk){
    sk = wi[sk];
    sk.add(sk.global, {
        dialog: function(chunk){
            var _t = this;
            
            _t.loading = new Image();
            _t.loading.src = sk.config.jUrl + 'loading.gif';
            _t.init = function(chunk){
                $(chunk).click(function(){                    
					var a = $(this).attr('href') || $(this).attr('alt');
					_t.show(a);
                    this.blur();
                    return false;
                });
                return false;
            };
            
            _t.show = function(url){
                try {
                    if (typeof document.body.style.maxHeight === "undefined") {
                        $("body", "html").css({
                            height: "100%",
                            width: "100%"
                        });
                        $("html").css("overflow", "hidden");
                        if (document.getElementById("dialog_hideSelect") === null) { //ie6 select !
                            $("body").append("<iframe id='dialog_hideSelect'></iframe><div id='dialog'><div id='dialog_wrap'><a id='dialog_closed'></a></div></div>");
                        }
                    }
                    else {
                        if (document.getElementById("dialog_overlay") === null) {
                            $("body").append("<div id='dialog'><div id='dialog_wrap'><a id='dialog_closed'></a></div></div>");
                        }
                    }
                    
                    $('#dialog').hide();
                    $("body").append("<div id='dialog_loading'><img src='" + _t.loading.src + "' /></div>");
                    $('#dialog_loading').show();
                    
                    var baseURL;
                    if (url.indexOf("?") !== -1) {
                        baseURL = url.substr(0, url.indexOf("?"));
                    }
                    else {
                        baseURL = url;
                    }
                    
                    var queryString = url.replace(/^[^\?]+\??/, '');
                    var params = _t.parseQuery(queryString);
                    
                    WIDTH = (params['width'] * 1) || 630; //defaults to 630 if no paramaters were added to URL
                    HEIGHT = (params['height'] * 1) || 440; //defaults to 440 if no paramaters were added to URL
                    B_WIDTH = WIDTH - 30;
					B_HEIGHT = HEIGHT - 30;
                    if (params['modal'] == "true") {
                        $("body").append("<div id='dialog_overlay'></div>");
                        $("#dialog_overlay").unbind();
                        $('#dialog_overlay').css({
                            'left': 0,
                            'top': 0,
                            'width': '100%',
                            'height': $(document).height()
                        }).show();
                    }
                    $("#dialog_wrap").append("<div id='dialog_content'></div>")
                    $("#dialog_content")[0].style.width = B_WIDTH + "px";
                    $("#dialog_content")[0].style.height = B_HEIGHT + "px";
                    $("#dialog_content")[0].scrollTop = 0;
                    $("#dialog_closed").click(_t.remove);
					url += url.indexOf("?") != -1 ? '&' : '?';
                    $("#dialog_content").load(url += "random=" + (new Date().getTime()), function(){
						$("#dialog_loading").remove();
                        _t.position();
						$("#dialog").show();                                                
                    });
                    
                    if (!params['modal']) {
						$('#dialog_closed').attr('title', '按Esc键也可以关闭哦');
                        document.onkeyup = function(e){
                            if (e == null) { // ie
                                keycode = event.keyCode;
                            }
                            else { // mozilla
                                keycode = e.which;
                            }
                            if (keycode == 27) { // close
                                _t.remove();
                            }
                        };
                    }
                } 
                catch (e) {
                    //
                }
            };
            
            _t.parseQuery = function(query){
                var Params = {};
                if (!query) {
                    return Params;
                }
                var Pairs = query.split(/[;&]/);
                for (var i = 0; i < Pairs.length; i++) {
                    var KeyVal = Pairs[i].split('=');
                    if (!KeyVal || KeyVal.length != 2) {
                        continue;
                    }
                    var key = unescape(KeyVal[0]);
                    var val = unescape(KeyVal[1]);
                    val = val.replace(/\+/g, ' ');
                    Params[key] = val;
                }
                return Params;
            };
            
            _t.remove = function(){
                $("#dialog_closed").unbind("click");
                $("#dialog").fadeOut("fast", function(){
                    $('#dialog_content,#dialog_wrap,#dialog_overlay,#dialog_hideSelect').trigger("unload").unbind().remove();
                });
				$("#dialog").remove();
                $("#dialog_loading").remove();
                if (typeof document.body.style.maxHeight == "undefined") {//if IE 6
                    $("body", "html").css({
                        height: "auto",
                        width: "auto"
                    });
                    $("html").css("overflow", "");
                }
                document.onkeydown = "";
                document.onkeyup = "";
                return false;
            };
            
            _t.position = function(){
                $("#dialog").css({
                    marginLeft: '-' + parseInt((WIDTH / 2), 10) + 'px',
                    width: WIDTH + 'px'
                });
                if (!(jQuery.browser.msie && jQuery.browser.version < 7)) { // take away IE6
                    $("#dialog").css({
                        marginTop: '-' + parseInt((HEIGHT / 2), 10) + 'px'
                    });
                }
            };
            
            return _t.init(chunk);
        }
    });
})(this, 'SKD');
