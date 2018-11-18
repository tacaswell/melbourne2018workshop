#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run


class Offset(PVGroup):
    offset = pvproperty(value=0, dtype=float)
    val = pvproperty(value=0, mock_record='ai')

    # Add the offset to any set value
    @val.putter
    async def val(self, instance, value):
        ...


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='offset:',
        desc="Counts up to infinity (well, integer oveflow)")
    ioc = Offset(**ioc_options)
    run(ioc.pvdb, **run_options)
