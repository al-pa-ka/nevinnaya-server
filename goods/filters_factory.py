from abc import ABC, abstractmethod


class FilterFactory(ABC):
    @abstractmethod
    def get_filters(self, data: dict) -> dict:...


class GoodFilterFactory(FilterFactory):
    def get_filters(self, data: dict) -> dict:
        if data.get('gender'):
            data['category__gender__in'] = [data.pop('gender'), 'UNIXEX']
        if data.get('category'):
            data['category__name'] = data.pop('category')
        return data

class DefaultFilterFactory(FilterFactory):
    def get_filters(self, data: dict) -> dict:
        return data
    