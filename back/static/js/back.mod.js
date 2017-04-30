/* 000001 */ 	(function () {
/* 000003 */ 		var login = function () {
/* 000004 */ 			var username = $ ("input[name='username']").val ();
/* 000005 */ 			var password = $ ("input[name='password']").val ();
/* 000006 */ 			var httpGet = function (theUrl) {
/* 000007 */ 				var xmlHttp = new XMLHttpRequest;
/* 000008 */ 				xmlHttp.open ('GET', theUrl, false);
/* 000009 */ 				xmlHttp.send (null);
/* 000010 */ 				return xmlHttp.status;
/* 000010 */ 			};
/* 000011 */ 			if (httpGet ('back/command=login;username={};password={}'.format (username, password)) == 200) {
/* 000012 */ 				$.cookie ('username', username);
/* 000013 */ 				return username;
/* 000013 */ 			}
/* 000014 */ 			else {
/* 000015 */ 				return false;
/* 000015 */ 			}
/* 000015 */ 		};
/* 000026 */ 		var logout = function () {
/* 000027 */ 			$.removeCookie ('username');
/* 000027 */ 		};
/* 000027 */ 		__pragma__ ('<all>')
/* 000027 */ 			__all__.login = login;
/* 000027 */ 			__all__.logout = logout;
/* 000027 */ 		__pragma__ ('</all>')
/* 000027 */ 	}) ();
/* 000027 */ 