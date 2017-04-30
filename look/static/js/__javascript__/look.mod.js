/* 000001 */ 	(function () {
/* 000003 */ 		var py_clear = function (id) {
/* 000004 */ 			$ ('#{}'.format (id)).py_clear ();
/* 000004 */ 		};
/* 000006 */ 		var hide = function (id) {
/* 000007 */ 			$ ('#{}'.format (id)).hide ();
/* 000007 */ 		};
/* 000009 */ 		var load = function (id, query) {
/* 000010 */ 			hide (id);
/* 000011 */ 			py_clear (id);
/* 000013 */ 			$.py_get ('html/{}'.format (query), __kwargtrans__ ({success: (function __lambda__ (d) {
/* 000014 */ 				return $ ('#{}'.format (id)).html (d);
/* 000016 */ 			}), error: load (id, 'command=error'), complete: show (id)}));
/* 000016 */ 		};
/* 000018 */ 		var show = function (id) {
/* 000019 */ 			$ ('#{}'.format (id)).show ();
/* 000019 */ 		};
/* 000019 */ 		__pragma__ ('<all>')
/* 000019 */ 			__all__.py_clear = py_clear;
/* 000019 */ 			__all__.hide = hide;
/* 000019 */ 			__all__.load = load;
/* 000019 */ 			__all__.show = show;
/* 000019 */ 		__pragma__ ('</all>')
/* 000019 */ 	}) ();
/* 000019 */ 