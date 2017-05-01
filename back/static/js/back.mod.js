/* 000001 */ 	(function () {
/* 000003 */ 		var login = function () {
/* 000004 */ 			var email = $ ("input[name='email']").val ();
/* 000005 */ 			var password = $ ("input[name='password']").val ();
/* 000006 */ 			print ('back login', email, password);
/* 000007 */ 			var httpGet = function (theUrl) {
/* 000008 */ 				var xmlHttp = new XMLHttpRequest;
/* 000009 */ 				xmlHttp.open ('GET', theUrl, false);
/* 000010 */ 				xmlHttp.send (null);
/* 000011 */ 				return tuple ([xmlHttp.status, xmlHttp.responseText]);
/* 000011 */ 			};
/* 000012 */ 			var __left0__ = httpGet ('back/?command=login&email={}&password={}'.format (email, password));
/* 000012 */ 			var status = __left0__ [0];
/* 000012 */ 			var text = __left0__ [1];
/* 000013 */ 			if (status == 200) {
/* 000014 */ 				$.cookie ('email', email);
/* 000015 */ 				$.cookie ('authtoken', text);
/* 000017 */ 				return email;
/* 000017 */ 			}
/* 000018 */ 			else {
/* 000019 */ 				return false;
/* 000019 */ 			}
/* 000019 */ 		};
/* 000021 */ 		var logout = function () {
/* 000022 */ 			$.removeCookie ('authtoken');
/* 000023 */ 			$.removeCookie ('email');
/* 000023 */ 		};
/* 000025 */ 		var signup = function () {
/* 000026 */ 			var email = $ ("input[name='email']").val ();
/* 000027 */ 			var password = $ ("input[name='password']").val ();
/* 000028 */ 			var csrfmiddlewaretoken = $ ("input[name='csrfmiddlewaretoken']").val ();
/* 000029 */ 			print ('back signup', email, password);
/* 000030 */ 			var httpGet = function (theUrl) {
/* 000031 */ 				var xmlHttp = new XMLHttpRequest;
/* 000032 */ 				xmlHttp.open ('POST', theUrl, false);
/* 000033 */ 				xmlHttp.setRequestHeader ('X-CSRFToken', $.cookie ('csrftoken'));
/* 000034 */ 				xmlHttp.send (null);
/* 000035 */ 				return xmlHttp.status;
/* 000035 */ 			};
/* 000036 */ 			if (httpGet ('back/?command=signup&email={}&password={}&csrfmiddlewaretoken={}'.format (email, password, csrfmiddlewaretoken)) == 200) {
/* 000037 */ 				return true;
/* 000037 */ 			}
/* 000038 */ 			else {
/* 000039 */ 				return false;
/* 000039 */ 			}
/* 000039 */ 		};
/* 000039 */ 		__pragma__ ('<all>')
/* 000039 */ 			__all__.login = login;
/* 000039 */ 			__all__.logout = logout;
/* 000039 */ 			__all__.signup = signup;
/* 000039 */ 		__pragma__ ('</all>')
/* 000039 */ 	}) ();
/* 000039 */ 