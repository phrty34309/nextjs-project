import logging

from wechatpy import exceptions as excs, WeChatClient as _WeChatClient

class WeChatClient(_WeChatClient):
    """继承原有WeChatClient添加日志功能"""
    def _request(self, method, url_or_endpoint, **kwargs):
        msg = self._log_msg(method, url_or_endpoint, **kwargs)
        self._logger("req").debug(msg)
        try:
            return super()._request(method, url_or_endpoint, **kwargs)
        except:
            self._logger("excs").warning(msg, exc_info=True)
            raise

    def _handle_result(self, res, method=None, url=None,
        *args, **kwargs):
        msg = self._log_msg(method, url, **kwargs)
        try:
            msg += "\tresp:" + res.content
        except:
            msg += "\tresp:{0}".format(res)
        return super()._handle_result(res, method, url, *args, **kwargs)

    def _logger(self, type):
        return logging.getLogger("wechat.api.{type}.{appid}".format(
            type=type, 
            appid=self.appid
        ))
    
    def _log_msg(self, method, url, **kwargs):
        msg = "{method}\t{url}".format(
            method=method,
            url=url
        )
        if kwargs.get("params"):
            msg += "\tparams:{0}".format(kwargs["params"])
        if kwargs.get("data"):
            msg += "\tdata:{0}".format(kwargs["data"])
        return msg