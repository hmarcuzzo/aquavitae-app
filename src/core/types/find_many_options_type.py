from src.core.types.find_one_options_type import FindOneOptions


class FindManyOptions(FindOneOptions, total=False):
    skip: int
    take: int
