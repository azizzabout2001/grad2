class StackOverflowMiddleware(object):
    def process_exception(self, request, exception):
        print exception.__class__.__name__
        print exception.message
        return None