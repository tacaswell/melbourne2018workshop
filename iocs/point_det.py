#!/usr/bin/env python3
from caproto.server import (pvproperty, PVGroup,
                            ioc_arg_parser, run)
import numpy as np
import asyncio
from textwrap import dedent


# this is a simplified version of the code in
# caproto.ioc_examples.mini_beamline
class PointDetector(PVGroup):
    """
    A coupled motor and point detector.  The measurement is
    a noise-free Gaussian centered around 0 with a σ of 5

    exp controls how long the 'exposure' takes

    Readonly PVs
    ------------
    det -> the detector value

    Settable PVs
    ------------
    mtr -> motor position
    exp -> exposure time

    """
    mtr = pvproperty(value=0, dtype=float)

    exp = pvproperty(value=1, dtype=float)

    @exp.putter
    async def exp(self, instance, value):
        value = np.clip(value, a_min=0, a_max=None)
        return value

    det = pvproperty(value=0, dtype=float, read_only=True)

    @det.getter
    async def det(self, instance):
        exposure_time = self.exp.value
        sigma = 5
        center = 0
        c = - 1 / (2 * sigma * sigma)
        m = self.mtr.value

        return exposure_time * np.exp((c * (m - center)**2))

    acq = pvproperty(value=0, dtype=float)
    busy = pvproperty(value=0, read_only=True)

    @acq.putter
    async def acq(self, instance, value):
        await self.busy.write(1)
        await asyncio.sleep(self.exp.value)
        await self.busy.write(0)
        return 0


if __name__ == '__main__':

    ioc_options, run_options = ioc_arg_parser(
        default_prefix='point:',
        desc=dedent(PointDetector.__doc__),
        # note this IOC only works with asycio due to the sleep
        supported_async_libs=('asyncio',))
    ioc = PointDetector(**ioc_options)
    run(ioc.pvdb, **run_options)
