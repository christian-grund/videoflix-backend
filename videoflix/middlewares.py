class AddAcceptRangesHeaderMiddleware:
    """
    Middleware that adds the 'Accept-Ranges' header to responses 
    for requests to media video files, indicating support for 
    byte-range requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/media/videos/'):
            response['Accept-Ranges'] = 'bytes'

        return response
