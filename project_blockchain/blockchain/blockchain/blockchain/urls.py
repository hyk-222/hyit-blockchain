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
# from blockchain_addr_tag import views as addr_tag
from blockchain_vpn import views as vpndc
from blockchain_tran_flow import views as flow



urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('now_transation', visualization.now_transaction),
   # path('transation_an', analysis.transaction_analysis),
    path('rank_value', visualization.RankValue),
    path('today_trade', visualization.Today_trade),
    path('map_data', visualization.MapData),
    path('bit_trade', visualization.Bit_trade),
    path('map_data2', visualization.MapData2),


    #path('recent_active_address', visualization.recent_active_address),
    path('transaction_pre_query', analysis.transaction_pre_query),
    path('transaction_next_query', analysis.transaction_next_query),
    path('transaction_txid_detail', analysis.transaction_txid_detail),
    path('transaction_address_detail', analysis.transaction_address_detail),
    path('transaction_address_all', analysis.address_all),

    path('pre_address', address.pre_address),
    path('next_address', address.next_address),

    # path('addrtag_Retrieve', addr_tag.addrtag_Retrieve),
    # path('addrtag_Search', addr_tag.addrtag_Search),
    path('recent_active_address', visualization.recent_active_address),

    ##虚拟货币使用记录页面功能
    path('vpn_insert', vpndc.InsertDB),  # 插入数据
    path('vpn_delete', vpndc.DeleteDB),  ##删除单条数据
    path('vpn_show', vpndc.vpn_show),  ##form展示
    path('vpn_query', vpndc.Query),  # 查询
    path('vpn_delete_M', vpndc.DeleteDB_multiple),  # 批量删除
    path('vpn_edit', vpndc.Edit),  ##修改数据
    path('vpn_insertexcel_u', vpndc.InsertExcel_u),  ##插入数据

    path('all_vpn_insert', vpndc.all_InsertDB),  # 插入数据
    path('all_vpn_show', vpndc.all_vpn_show),  ##form展示
    path('all_vpn_query', vpndc.all_Query),  # 查询
    path('all_vpn_edit', vpndc.all_Edit),  ##修改数据
    path('all_vpn_insertexcel_u', vpndc.all_InsertExcel_u),  ##插入数据
    path('all_vpn_delete', vpndc.all_DeleteDB),  ##删除单条数据
    path('all_vpn_delete_M', vpndc.all_DeleteDB_multiple),  # 批量删除

    ##交易流水功能
    path('flow_show', flow.flow_show),  # 插入数据
    path('to_view', flow.to_view),  # 查看详情数据
    path('delete_records', flow.delete_records),
    path('expore_file', flow.expore_file),

    ##地址监控
    # path('addr_monitor_show', addr_tag.addr_monitor_show),
    # path('addr_monitor_delete', addr_tag.addr_monitor_delete),
    # path('addr_monitor_delete_M', addr_tag.addr_monitor_delete_M),
    # path('addr_monitor_edit', addr_tag.addr_monitor_edit),
    # path('addrtag_query', addr_tag.addrtag_query),
    # path('addr_monitor_insert', addr_tag.addr_monitor_insert),

    # 地址标注
    # path('addrtag_show', addr_tag.addrtag_show),
    # path('addrtag_delete', addr_tag.addrtag_delete),
    # path('addrtag_delete_M', addr_tag.addrtag_delete_M),
    # path('addrtag_edit', addr_tag.addrtag_edit),
    # path('addrtag_query', addr_tag.addrtag_query),
    # path('addrtag_insert', addr_tag.addrtag_insert),




]
