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
/* 000011 */ 		var hookLogin = function () {
/* 000012 */ 			hide ('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard');
/* 000013 */ 			var username = back.login ();
/* 000014 */ 			clean ('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard');
/* 000015 */ 			if (!(username)) {
/* 000016 */ 				loadMessage ('badnews', 'Non è stato possibile accedere. Ritenta o contatta il tuo insegnante.');
/* 000017 */ 				show ('badnews');
/* 000017 */ 			}
/* 000018 */ 			load ('navbar', 'command=navbar;username={}'.format (username));
/* 000019 */ 			load ('welcomeBoard', 'command=welcomeBoard;username={}'.format (username));
/* 000020 */ 			show ('navbar', 'welcomeBoard');
/* 000020 */ 		};
/* 000022 */ 		var hookLogout = function () {
/* 000023 */ 			clean ('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard');
/* 000024 */ 			back.logout ();
/* 000025 */ 			show ('loadingBoard');
/* 000026 */ 			load ('navbar', 'command=navbar');
/* 000027 */ 			load ('welcomeBoard', 'command=welcomeBoard');
/* 000028 */ 			show ('welcomeBoard');
/* 000029 */ 			hide ('loadingBoard');
/* 000029 */ 		};
/* 000031 */ 		var load = function (id, query) {
/* 000032 */ 			print ('load', id, query);
/* 000033 */ 			clean (id);
/* 000036 */ 			$.ajax (dict ({'method': 'GET', 'url': 'html/{}'.format (query), 'success': (function __lambda__ (d) {
/* 000037 */ 				return $ ('#{}'.format (id)).html (d);
/* 000037 */ 			}), 'error': (function __lambda__ (d) {
/* 000038 */ 				return load (id, 'command=error');
/* 000038 */ 			})}));
/* 000038 */ 		};
/* 000040 */ 		var loadMessage = function (id, msg) {
/* 000041 */ 			load (id, 'command=message;message={}'.format (encodeURIComponent (msg)));
/* 000041 */ 		};
/* 000043 */ 		var show = function () {
/* 000043 */ 			var args = tuple ([].slice.apply (arguments).slice (0));
/* 000044 */ 			var __iterable0__ = args;
/* 000044 */ 			for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
/* 000044 */ 				var id = __iterable0__ [__index0__];
/* 000045 */ 				$ ('#{}'.format (id)).show ();
/* 000045 */ 			}
/* 000045 */ 		};
/* 000047 */ 		var username = $.cookie ('username');
/* 000048 */ 		load ('navbar', 'command=navbar;username={}'.format (username));
/* 000049 */ 		load ('welcomeBoard', 'command=welcomeBoard;username={}'.format (username));
/* 000050 */ 		show ('welcomeBoard');
/* 000051 */ 		hide ('loadingBoard');
/* 000051 */ 		__pragma__ ('<all>')
/* 000051 */ 			__all__.clean = clean;
/* 000051 */ 			__all__.hide = hide;
/* 000051 */ 			__all__.hookLogin = hookLogin;
/* 000051 */ 			__all__.hookLogout = hookLogout;
/* 000051 */ 			__all__.load = load;
/* 000051 */ 			__all__.loadMessage = loadMessage;
/* 000051 */ 			__all__.show = show;
/* 000051 */ 			__all__.username = username;
/* 000051 */ 		__pragma__ ('</all>')
/* 000051 */ 	}) ();
/* 000051 */ 