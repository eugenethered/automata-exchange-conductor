import logging
from typing import List, Optional

from config.report.holder.ConfigReporterHolder import ConfigReporterHolder
from core.exchange.InstrumentExchange import InstrumentExchange
from core.market.Market import Market
from core.missing.Context import Context
from exchangetransformrepo.ExchangeTransform import ExchangeTransform
from exchangetransformrepo.repository.ExchangeTransformRepository import ExchangeTransformRepository
from missingrepo.Missing import Missing
from utility.json_utility import as_data

from conductor.extractor.DataExtractor import DataExtractor


class ExchangeTransformer:

    def __init__(self, market: Market, repository: ExchangeTransformRepository, data_extractor: DataExtractor):
        self.market = market
        self.repository = repository
        self.data_extractor = data_extractor
        self.config_reporter = ConfigReporterHolder()

    def transform(self, exchange_instrument_data) -> Optional[InstrumentExchange]:
        transformations = self.load_transformations()
        raw_instrument = self.data_extractor.extract(exchange_instrument_data)
        if raw_instrument in transformations:
            exchange_transformation = transformations[raw_instrument]
            return self.transform_to_instrument_exchange(exchange_transformation)
        else:
            self.report_missing_instrument_exchange(raw_instrument)
            return None

    def load_transformations(self):
        exchange_transformations = self.repository.retrieve()
        return dict(self.unpack_transformations(exchange_transformations))

    @staticmethod
    def unpack_transformations(exchange_transformations: List[ExchangeTransform]):
        for exchange_transform in exchange_transformations:
            yield exchange_transform.instrument, exchange_transform

    def transform_to_instrument_exchange(self, exchange_transformation):
        if exchange_transformation.ignore is True:
            return None
        (instruments, invert) = self.extract_transform_constituents(exchange_transformation.transform)
        (instrument, to_instrument) = tuple(instruments.split('/'))
        return InstrumentExchange(instrument, to_instrument)

    @staticmethod
    def extract_transform_constituents(transform):
        return as_data(transform, 'instruments'), as_data(transform, 'invert', False)

    def report_missing_instrument_exchange(self, raw_instrument):
        def log_missing():
            logging.warning(f'No transformation for raw instrument:{raw_instrument}')
        missing = Missing(raw_instrument, Context.EXCHANGE, self.market, f'Missing instrument:[{raw_instrument}]')
        self.config_reporter.report_missing(missing, log_missing)