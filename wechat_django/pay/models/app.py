# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models as m
from django.utils.translation import ugettext_lazy as _

from wechat_django.models import WeChatApp
from ..client import WeChatPayClient


class WeChatPay(m.Model):
    app = m.OneToOneField(
        WeChatApp, on_delete=m.CASCADE, primary_key=True,
        related_name="pay")

    mch_id = m.CharField(
        _("mch_id"), max_length=32,
        help_text=_("微信支付分配的商户号"))
    api_key = m.CharField(
        _("WeChatPay api_key"), max_length=128,
        help_text=_("商户号key"))

    sub_mch_id = m.CharField(
        _("sub_mch_id"), max_length=32, blank=True, null=True,
        help_text=_("子商户号，受理模式下填写"))
    mch_app_id = m.CharField(
        _("mch_app_id"), max_length=32,
        help_text=_("微信分配的公众账号ID，受理模式下填写"),
        blank=True, null=True)

    mch_cert = m.BinaryField(_("mch_cert"), blank=True, null=True)
    mch_key = m.BinaryField(_("mch_key"), blank=True, null=True)

    @property
    def appid(self):
        return self.mch_app_id if self.mch_app_id else self.app.appid

    @property
    def sub_appid(self):
        return self.app.appid if self.mch_app_id else None

    class Meta(object):
        verbose_name = _("WeChat pay")
        verbose_name_plural = _("WeChat pay")

    @property
    def name(self):
        return self.app.name

    @property
    def client(self):
        """:rtype: wechat_django.client.WeChatPayClient"""
        if not hasattr(self, "_client"):
            self._client = WeChatPayClient(self)
        return self._client

    def __str__(self):
        return str(self.app)
