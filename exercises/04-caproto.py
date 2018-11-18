#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run


class Simple(PVGroup):
    a = pvproperty(value=0)
    b = pvproperty(value=0)


# we want to have the PVs:
#   nested:one:a
#   nested:one:b
#   nested:two:a
#   nested:two:b
class Nested(PVGroup):
    one = ...
    two = ...


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='nested:',
        desc="Counts up to infinity (well, integer oveflow)")
    ioc = Nested(**ioc_options)
    run(ioc.pvdb, **run_options)
