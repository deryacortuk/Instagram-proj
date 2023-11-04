from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSiteMap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'
    
    def items(self):
        return ["account:home","account:sample_user","account:about","account:faq","account:pricing"]
    def location(self,item):
        return reverse(item)