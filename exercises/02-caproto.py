#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
import time


class ForeverCounter(PVGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # make unsigned
    val = pvproperty(value=0, mock_record='ai')

    # increment no more than once a second
    @val.scan(period=.1, use_scan_field=True)
    async def val(self, instance, async_lib):
        current_time = time.monotonic()


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='counter:',
        desc="Counts up to infinity (well, integer oveflow)")
    ioc = ForeverCounter(**ioc_options)
    run(ioc.pvdb, **run_options)
