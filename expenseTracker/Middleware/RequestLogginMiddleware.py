from tracker.models import *

class RequestLogging:
    
    def __init__(self,get_response):
        self.get_response=get_response
        # print('get_response: ',get_response)
        
    def __call__(self, request):
        request_info=request
        # print('request_info=',request_info)
        # print('path = ',request_info.path , 'method=',request_info.method)
        # print('self.get_response(request_info) = ',self.get_response(request_info))
        
        RequestLogs.objects.create(
            request_info=vars(request_info),
            request_type=request_info.method,
            request_method=request_info.path,
        )
        return self.get_response(request_info)
    
    