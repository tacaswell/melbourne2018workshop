#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run


class AccessCounter(PVGroup):
    val = pvproperty(value=0, dtype=float)

    # fill in so that there read-only counters of how many times
    # the value is read or put to
    read_counter = ...
    write_counter = ...

    @val.putter
    async def val(self, instance, value):
        ...

    @val.getter
    async def val(self, instance):
        ...


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='access_counter:',
        desc="counts how many times the PV is accessed")
    ioc = AccessCounter(**ioc_options)
    run(ioc.pvdb, **run_options)
