(function () {
    "use strict";
    window.puppy = {};

    puppy.ajax = function (url, method, payload, headers) {
        var acceptableMethods = {GET: true, POST: true, PUT: true, DELETE: true}, options;

        method = method.toUpperCase(); // just in case.

        if (!acceptableMethods[method]) {
            throw Error('Unknown method. Acceptable methods: ' + Object.keys(acceptableMethods).join(', '));
        }

        options = {
            url: url,
            type: method,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        };

        if (headers) {
            options.headers = headers;
        }

        if (method === 'GET') {
            if (payload) {
                throw Error('A GET request cannot have a payload.');
            }
        } else {
            options.data = JSON.stringify(payload);
        }

        return $.ajax(options);
    };

    puppy.getJSON = function (url) {
        return puppy.ajax(url, 'GET');
    };

    puppy.postJSON = function (url, payload) {
        return puppy.ajax(url, 'POST', payload);
    };

    puppy.putJSON = function (url, payload) {
        return puppy.ajax(url, 'PUT', payload);
    };

    puppy.deleteJSON = function(url, payload) {
        return puppy.ajax(url, 'DELETE', payload);
    };
})();