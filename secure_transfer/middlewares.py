class UserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            current_agent = request.META["HTTP_USER_AGENT"]
            if user.user_agent != current_agent:
                user.user_agent = current_agent
                user.save()

        response = self.get_response(request)
        return response