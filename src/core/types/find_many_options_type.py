from src.core.types.find_one_options_type import FindOneOptions


class FindManyOptions(FindOneOptions):
    skip: int
    take: int
