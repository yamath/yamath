/* 000001 */ 	(function () {
/* 000003 */ 		var clean = function () {
/* 000003 */ 			var args = tuple ([].slice.apply (arguments).slice (0));
/* 000004 */ 			var __iterable0__ = args;
/* 000004 */ 			for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
/* 000004 */ 				var id = __iterable0__ [__index0__];
/* 000005 */ 				$ ('#{}'.format (id)).empty ();
/* 000005 */ 			}
/* 000005 */ 		};
/* 000007 */ 		var hide = function () {
/* 000007 */ 			var args = tuple ([].slice.apply (arguments).slice (0));
/* 000008 */ 			var __iterable0__ = args;
/* 000008 */ 			for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
/* 000008 */ 				var id = __iterable0__ [__index0__];
/* 000009 */ 				$ ('#{}'.format (id)).hide ();
/* 000009 */ 			}
/* 000009 */ 		};
/* 000031 */ 		var hookProfile = function () {
/* 000032 */ 			clean ('goodnews', 'badnews', 'welcomeBoard');
/* 000033 */ 			hide ('goodnews', 'badnews', 'welcomeBoard');
/* 000034 */ 			load ('activeBoard', 'command=profile');
/* 000035 */ 			show ('activeBoard');
/* 000035 */ 		};
/* 000052 */ 		var load = function (id, query) {
/* 000053 */ 			print ('load', id, query);
/* 000054 */ 			clean (id);
/* 000057 */ 			$.ajax (dict ({'method': 'GET', 'url': 'html/?{}'.format (query), 'success': (function __lambda__ (d) {
/* 000058 */ 				return $ ('#{}'.format (id)).html (d);
/* 000058 */ 			}), 'error': (function __lambda__ (d) {
/* 000059 */ 				return load (id, 'command=error');
/* 000059 */ 			})}));
/* 000059 */ 		};
/* 000061 */ 		var loadMessage = function (id, msg) {
/* 000062 */ 			load (id, 'command=message&message={}'.format (encodeURIComponent (msg)));
/* 000062 */ 		};
/* 000064 */ 		var show = function () {
/* 000064 */ 			var args = tuple ([].slice.apply (arguments).slice (0));
/* 000065 */ 			var __iterable0__ = args;
/* 000065 */ 			for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
/* 000065 */ 				var id = __iterable0__ [__index0__];
/* 000066 */ 				$ ('#{}'.format (id)).show ();
/* 000066 */ 			}
/* 000066 */ 		};
/* 000068 */ 		load ('navbar', 'command=navbar');
/* 000069 */ 		load ('welcomeBoard', 'command=welcomeBoard');
/* 000070 */ 		show ('welcomeBoard');
/* 000071 */ 		hide ('loadingBoard');
/* 000071 */ 		__pragma__ ('<all>')
/* 000071 */ 			__all__.clean = clean;
/* 000071 */ 			__all__.hide = hide;
/* 000071 */ 			__all__.hookProfile = hookProfile;
/* 000071 */ 			__all__.load = load;
/* 000071 */ 			__all__.loadMessage = loadMessage;
/* 000071 */ 			__all__.show = show;
/* 000071 */ 		__pragma__ ('</all>')
/* 000071 */ 	}) ();
/* 000071 */ 