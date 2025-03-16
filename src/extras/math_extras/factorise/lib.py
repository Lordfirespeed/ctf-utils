from utils.typedefs.factorise import *


def combine_factors_left(sink: PrimeFactorisation, source: PrimeFactorisation) -> PrimeFactorisation:
    for source_factor, source_factor_exponent in source.items():
        sink_factor_exponent = sink.get(source_factor, 0)
        sink[source_factor] = sink_factor_exponent + source_factor_exponent
    return sink


__all__ = ("combine_factors_left",)
