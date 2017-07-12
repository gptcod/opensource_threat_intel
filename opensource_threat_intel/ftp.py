import json

from scrapy.core.downloader.handlers.ftp import FTPDownloadHandler
from scrapy.http import Response
from twisted.protocols.ftp import FTPFileListProtocol

from spiders.cyren_intel import FileFtpRequest, ListFtpRequest


class FtpListingHandler(FTPDownloadHandler):
    # get files list or one file
    def gotClient(self, client, request, filepath):
        # check what class sent a request
        if isinstance(request, FileFtpRequest):
            return super(FtpListingHandler, self).gotClient(
                client, request, filepath)

        protocol = FTPFileListProtocol()
        return client.list(filepath, protocol).addCallbacks(
            callback=self._build_response,
            callbackArgs=(request, protocol),
            errback=self._failed,
            errbackArgs=(request,))

    def _build_response(self, result, request, protocol):
        # get files list or one file
        self.result = result
        if isinstance(request, ListFtpRequest):
            body = json.dumps(protocol.files)
            return Response(url=request.url, status=200, body=body)
        # signal file return super class _build_response result
        else:
            return super(FtpListingHandler, self)._build_response(
                result, request, protocol)
