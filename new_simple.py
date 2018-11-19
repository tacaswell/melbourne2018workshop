#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
import time
import random

class SimpleIOC(PVGroup):
    "An IOC with two simple read/writable PVs"
    A = pvproperty(value=1)
    B = pvproperty(value=2)
    # ADDED THIS LINE
    C = pvproperty(value=2.0, dtype=float, precision=5)

    @C.putter
    async def C(self, instance, value):
        print("I got value ", value)

        return max(.1, value)

    @C.getter
    async def C(self, instance):
        print("Hi Mom!")

    D = pvproperty(value=0.0, dtype=float, read_only=True)

    @D.getter
    async def D(self, instance):
        await self.C.write(random.random() * self.A.value)
        return time.time()


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='simple:',
        desc="Run an IOC with two simple, uncoupled, readable/writable PVs.")
    ioc = SimpleIOC(**ioc_options)
    run(ioc.pvdb, **run_options)
