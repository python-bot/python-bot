#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a simple echo bot using decorators and webhook with BaseHTTPServer
# It echoes any incoming text messages and does not use the polling method.

from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
from threading import Thread

from python_bot.bot.bot import bot_logger
from python_bot.common.webhook.handlers.base import BaseWebHookHandler
from python_bot.settings import WebHookSettings


class PythonHandler(BaseWebHookHandler):
    def __init__(self, settings: WebHookSettings, handlers):
        self._server_class = self.__get_server_class()
        self.__server_thread = None
        self.__server = None
        super().__init__(settings, handlers)

    def __get_server_class(self):
        that = self

        class WebhookHandler(BaseHTTPRequestHandler):
            server_version = "WebhookHandler/1.0"

            def __process(self, request_type):
                try:
                    if 'content-type' in self.headers or 'content-length' in self.headers:
                        handler = that.get_request_handler(request_type, self.path, self.headers)
                        if handler:
                            # todo for get
                            data = self.rfile.read(int(self.headers['content-length']))
                            handler.process(data)

                    self.send_response(200)
                except:
                    bot_logger.exception("Exception during processing request")
                    self.send_error(500)
                finally:
                    self.end_headers()

            def do_HEAD(self):
                self.__process("HEAD")

            def do_GET(self):
                self.__process("GET")

            def do_PATCH(self):
                self.__process("PATCH")

            def do_PUT(self):
                self.__process("PUT")

            def do_POST(self):
                self.__process("POST")

        return WebhookHandler

    def __start_server(self):
        self.__server = HTTPServer((self.settings.listen, self.settings.port),
                                   self._server_class)

        self.__server.socket = ssl.wrap_socket(self.__server.socket,
                                               certfile=self.settings.ssl_cert,
                                               keyfile=self.settings.ssl_private,
                                               server_side=True)

        self.__server.serve_forever()

    def start(self):
        bot_logger.debug("Starting http server")
        if self.__server_thread:
            bot_logger.debug("Calling start before stop")
            self.stop()
        self.__server_thread = Thread(target=self.__start_server)
        self.__server_thread.daemon = True  # Do not make us wait for you to exit
        self.__server_thread.start()

    def stop(self):
        bot_logger.debug("Stopping http server")
        if not self.__server:
            bot_logger.debug("Server is not running")
            return
        if not self.__server_thread:
            bot_logger.debug("Server thread is not running")
            return

        self.__server.shutdown()
