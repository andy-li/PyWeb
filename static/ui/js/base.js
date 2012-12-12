(function(wi, g, $, undef){
    wi[g] = wi[g] || {};
    wi[$] = $;
    var sk = wi[g];
    
    sk.config = sk.config || {};
    
    sk.add = function(r, s, ov) {
        if (!s || !r) 
            return r;
        if (ov == undef) 
            ov = true;
        var i;
        for (i in s) {
            if (ov || !(i in r)) {
                r[i] = s[i];
            }
        }
        return r;
    };
    
	sk.clone = function(o) {
		if(typeof o !== 'object') return false;
		
		function clone() {
			
		};
		
		clone.prototype = o;
		
		var s = new clone();
		for(i in s) {
			if(typeof s[i] === 'object') {
				s[i] = sk.clone(s[i]);
			}
		}
		return s;
	};
	
    sk.ready = function(fn) {
        $(document).ready(fn);
        return this;
    };
    
    sk.version = '0.1';
    
})(this, 'SKD', jQuery);

(function(wi, sk){
    sk = wi[sk];
    
    sk.add(sk.config, {
        domain: 'http://127.0.0.1:8001/',
        jUrl: 'http://localhost/pagemanage/static/ui/js/'
    });
    
    sk.add(sk, {
        global: {}
    });
	
    sk.add(sk.global, {
        notEmptyArray: function(ary) {
            return $.isArray(ary) && ary.length > 0;
        },
        queue: function(o, s) {
            o = (typeof o == "object") ? o : $(o);
            
            if (sk.global.notEmptyArray(s)) {
                var M = "obj_Queue";
                
                s.push(function() {
                    o.clearQueue(M);
                });
                o.queue(M, s);
                $.each(s, function() {
                    o.dequeue(M);
                });
            }
        },
		
        request: function(paras){
            var url = window.location.href;
            var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&");
            var paraObj = {};
            for (i = 0; j = paraString[i]; i++) {
                paraObj[j.substring(0, j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf("=") + 1, j.length);
            }
            var result = paraObj[paras.toLowerCase()];
            if (typeof result == 'undefined') {
                return '';
            }
            else {
                return result;
            }
        }
    });
    
    sk.add(sk, {
        loader: {}
    });
    sk.add(sk.loader, {
        require: function(module, fn) {        
            var scripts = [], url;
            
            function getScript(url) {
                var script = scripts[url];
                if (!script) {
                    script = {
                        loaded: false,
                        funs: []
                    };
                    scripts[url] = script;
                    add(script, url);
                }
                
                return script;
            }
            
            function run(script) {
                var funs = script.funs, len = funs.length, i = 0;
                for (; i < len; i++) {
                    var fun = funs.pop();
                    fun();
                }
            }
            
            function add(script, url) {
                var scriptdom = document.createElement('script');
                scriptdom.type = 'text/javascript';
                scriptdom.loaded = false;
                scriptdom.src = url;
                
                scriptdom.onload = function() {
                    scriptdom.loaded = true;
                    run(script);
                    scriptdom.onload = scriptdom.onreadystatechange = null;
                };
                
                scriptdom.onreadystatechange = function() {
                    if ((scriptdom.readyState === 'loaded' ||
                    scriptdom.readyState === 'complete') &&
                    !scriptdom.loaded) {
                    
                        run(script);
                        scriptdom.onload = scriptdom.onreadystatechange = null;
                    }
                };
                
                document.getElementsByTagName('head')[0].appendChild(scriptdom);
            }
			
            
            function load(url, fn) {
                var script = getScript(url), loaded = script.loaded;
                
                if (typeof fn === 'function') {
                    if (loaded) {
                        fn();
                    }
                    else {
                        script.funs.push(fn);
                    }
                }
            }
			
			function jsUrl(module) {				 
				return sk.config.jUrl + module.replace(/\./gi, '/') + '.js';
			}
            
            load(jsUrl(module), fn);
        }
    });
	
})(this, 'SKD');