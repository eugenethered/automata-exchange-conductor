import logging

from conductor.instrument.InstrumentExchangeHandler import InstrumentExchangeHandler
from conductor.provider.ExchangeDataProvider import ExchangeDataProvider
from conductor.transform.ExchangeTransformer import ExchangeTransformer


class ExchangeConductor:

    def __init__(self, options, transformer: ExchangeTransformer, data_provider: ExchangeDataProvider, handler: InstrumentExchangeHandler):
        self.options = options
        self.transformer = transformer
        self.data_provider = data_provider
        self.handler = handler

    def get_instrument_exchanges(self):
        exchange_instruments_payload = self.data_provider.fetch_exchange_instruments()
        logging.info(f'Obtained raw exchange instruments[{len(exchange_instruments_payload)}]')
        for exchange_instrument_data in exchange_instruments_payload:
            instrument_exchange = self.transformer.transform(exchange_instrument_data)
            self.handler.handle_instrument_exchange(instrument_exchange)
