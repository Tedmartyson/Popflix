from django.contrib import admin

from catalog.models import House, Auction

class HouseAdmin(admin.ModelAdmin):
    pass

class AuctionAdmin(admin.ModelAdmin):
    pass

admin.site.register(House, HouseAdmin)
admin.site.register(Auction, AuctionAdmin)
