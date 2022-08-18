"""blockchain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from blockchain_visualization import views as visualization



from blockchain_transaction import views as analysis
from blockchain_address import views as address
from blockchain_addr_tag import views as addr_tag
from blockchain_vpn import views as vpndc



urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('now_transation', visualization.now_transaction),
   # path('transation_an', analysis.transaction_analysis),
    ##数据大屏展示
    path('address', address.address),
    path('address_search', address.address_search),
    path('rank_value', visualization.RankValue),
    path('today_trade', visualization.Today_trade),
    path('map_data', visualization.MapData),
    path('bit_trade',visualization.Bit_trade),
    path('map_data2', visualization.MapData2),

    #比特币交易可视化
    #path('recent_active_address', visualization.recent_active_address),
    path('transation_an', analysis.transaction_analysis),
    path('transaction_search', analysis.transaction_search),
    path('transaction_search2', analysis.transaction_search2),
    path('transaction_search_input', analysis.transaction_search_input),
    path('transaction_search_output', analysis.transaction_search_output),
    path('transaction_pre_query', analysis.transaction_pre_query),
    path('transaction_next_query', analysis.transaction_next_query),
    #有点乱，未知
    path('addrtag_Retrieve', addr_tag.addrtag_Retrieve),
    path('addrtag_Search', addr_tag.addrtag_Search),
    path('recent_active_address',visualization.recent_active_address),#前端首页最近区块


    ##vpn页面功能
    path('vpn_insert',vpndc.InsertDB),#插入数据
    path('vpn_delete',vpndc.DeleteDB),##删除单条数据
    path('vpn_show',vpndc.vpn_show),##form展示
    #path('vpn_query',vpndc.Query),#查询
    path('vpn_query',vpndc.Query),#查询
    path('vpn_delete_M',vpndc.DeleteDB_multiple),#批量删除
    path('vpn_edit',vpndc.Edit),##修改数据
    path('vpn_insertexcel_u',vpndc.InsertExcel_u),##插入数据


]
