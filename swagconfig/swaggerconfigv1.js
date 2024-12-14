window.onload = function () {
    SwaggerUIBundle({
        url: "/swagconfig.json",
        dom_id: '#swagger-ui',
        syntaxHighlight: false,
        syntaxHighlightTheme: null,

        responseInterceptor: function (response) {
            response.text = JSON.stringify(JSON.parse(response.text), null, 2);
            return response;
        },

        requestInterceptor: function (request) {
            request.headers['Accept'] = 'application/json, text/plain';
            return request;
        },
    });
};