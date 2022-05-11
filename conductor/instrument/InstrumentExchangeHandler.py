from core.exchange.InstrumentExchange import InstrumentExchange
from exchangerepo.repository.InstrumentExchangeRepository import InstrumentExchangeRepository


class InstrumentExchangeHandler:

    def __init__(self, repository: InstrumentExchangeRepository):
        self.repository = repository

    # todo: not very performant (practical for now)
    def handle_instrument_exchange(self, instrument_exchange: InstrumentExchange):
        instrument_exchanges_holder = self.repository.retrieve()
        instrument_exchanges_holder.add(instrument_exchange)
        self.repository.store(instrument_exchanges_holder)
