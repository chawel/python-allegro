# coding=utf-8
"""
The After Sale Service Conditions endpoint


Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi
from .aftersalesserviceconditionreturnpolicies import AfterSaleServiceConditionReturnPolicies
from .aftersalesserviceconditionsimpliedwarranties import AfterSaleServiceConditionImpliedWarranties
from .aftersalesserviceconditionswarranties import AfterSaleServiceConditionWarranties


class AfterSaleServiceConditions(BaseApi):
    """
    Base Endpoint
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(AfterSaleServiceConditions, self).__init__(*args, **kwargs)
        self.endpoint = 'after-sales-service-conditions'
        self.return_policies = AfterSaleServiceConditionReturnPolicies(self)
        self.implied_warranties = AfterSaleServiceConditionImpliedWarranties(self)
        self.warranties = AfterSaleServiceConditionWarranties(self)
