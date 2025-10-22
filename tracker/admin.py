from django.contrib import admin
from tracker.models import *


#TO change the site-header in the django admin
admin.site.site_header = " Expense Tracker"
admin.site.site_title = "Expense Tracker"
admin.site.site_url = "Expense Tracker"

# registering CurrentBalance model to admin panel
class CurrentBal(admin.ModelAdmin):
    list_display=['user','current_balance']
admin.site.register(CurrentBalance,CurrentBal)


# Thsi is for making admin panel to display data in table form

class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display=[
        'amount','current_balance','description','expense_type','created_at','display_typeof_amt'
    ]


    #create dynamic field which is not in model and should include means
    def display_typeof_amt(self,obj):
        if obj.amount<0:
            return "Negative"
        return "Positive"
    
    #adding search field on particular column name
    search_fields=['expense_type','created_at','amount']

    #ordering the display
    ordering=['-created_at']

    # adding filters
    list_filter=['expense_type']




# registering TrackingHistory model to admin panel
admin.site.register(TrackingHistory,TrackingHistoryAdmin)