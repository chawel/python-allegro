# coding=utf-8

# allegroapi
# Copyright 2018 Pawel Chaniewski
# See LICENSE for details.

"""
Allegro.pl REST API Wrapper
"""
__version__ = '1.0.0'
__author__ = 'Pawel Chaniewski'
__license__ = 'MIT'

# API Client
from .allegroclient import AllegroClient

# API Root
from .entities.root import Root
# Offers
from .entities.offers import Offers
from .entities.offerchangepricecommands import OfferChangePriceCommands
from .entities.offerrenewcommands import OfferRenewCommands
# Sale
from .entities.sale import Sale
from .entities.saleoffers import SaleOffers
from .entities.salecategories import SaleCategories
from .entities.salecategoryparameters import SaleCategoryParameters
from .entities.saleshippingrates import SaleShippingRates
from .entities.saleoffervariants import SaleOfferVariants
from .entities.saleofferpublicationcommands import SaleOfferPublicationCommands
from .entities.saleofferpublicationcommandtasks import SaleOfferPublicationCommandTasks
# Sale images
from .entities.saleimages import SaleImages
# After-sale
from .entities.aftersalesserviceconditions import AfterSaleServiceConditions
from .entities.aftersalesserviceconditionswarranties import AfterSaleServiceConditionWarranties
from .entities.aftersalesserviceconditionsimpliedwarranties import AfterSaleServiceConditionImpliedWarranties
from .entities.aftersalesserviceconditionreturnpolicies import AfterSaleServiceConditionReturnPolicies
# Users
from .entities.users import Users
from .entities.userratingssummary import UserRatingsSummary


class Allegro(AllegroClient):
    """
    Allegro.pl class to communicate with the REST API
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class with your api_key and user_id and attach all of
        the endpoints
        """
        super(Allegro, self).__init__(*args, **kwargs)
        # API Root
        self.root = self.api_root = Root(self)
        # Offers
        self.offers = Offers(self)
        self.offers.change_price_commands = OfferChangePriceCommands(self)
        self.offers.renew_commands = OfferRenewCommands(self)
        # Sale
        self.sale = Sale(self)
        self.sale.offers = SaleOffers(self)
        self.sale.offer_variants = SaleOfferVariants(self)
        self.sale.categories = SaleCategories(self)
        self.sale.categories.parameters = SaleCategoryParameters(self)
        self.sale.shipping_rates = SaleShippingRates(self)
        # Sale Command
        self.sale.offer_publication_commands = SaleOfferPublicationCommands(self)
        self.sale.offer_publication_commands.tasks = SaleOfferPublicationCommandTasks(self)
        # Sale Images
        self.sale.images = SaleImages(self)
        # After-sale
        self.after_sale_conditions = AfterSaleServiceConditions(self)
        self.after_sale_conditions.warranties = AfterSaleServiceConditionWarranties(self)
        self.after_sale_conditions.implied_warranties = AfterSaleServiceConditionImpliedWarranties(self)
        self.after_sale_conditions.return_policies = AfterSaleServiceConditionReturnPolicies(self)
        # Users
        self.users = Users(self)
        self.users.ratings_summary = UserRatingsSummary(self)
