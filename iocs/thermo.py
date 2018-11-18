#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
from caproto import ChannelType
import numpy as np
import time
from textwrap import dedent


class Thermo(PVGroup):
    """
    Simulates (poorly) an oscillating temperature controller.

    Follows :math:`T_{output} = T_{var} exp^{-(t - t_0)/K} sin(ω t) + T_{setpoint}`

    The default prefix is `thermo:`

    Readonly PVs
    ------------

    I -> the current value

    Control PVs
    -----------

    SP -> where to go
    K -> the decay constant
    omega -> the oscillation frequency
    Tvar -> the scale of the oscillations
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._T0 = time.monotonic()
        self._entered_band = -1

    readback = pvproperty(value=0, dtype=float, read_only=True,
                          name='I',
                          mock_record='ai', units='K')

    setpoint = pvproperty(value=100, dtype=float, name='SP',
                          mock_record='ai', units='K')
    K = pvproperty(value=10, dtype=float, units='1/K')
    omega = pvproperty(value=np.pi, dtype=float, units='Hz')
    Tvar = pvproperty(value=10, dtype=float, units='K')

    state = pvproperty(value=0, dtype=ChannelType.ENUM,
                       enum_strings=['stable', 'settling'],
                       read_only=True)
    deadband = pvproperty(value=2, dtype=float)
    settle_time = pvproperty(value=2, dtype=float, units='s')

    @readback.scan(period=.1, use_scan_field=True)
    async def readback(self, instance, async_lib):

        def t_rbv(T0, setpoint, K, omega, Tvar,):
            t = time.monotonic()
            return ((Tvar *
                     np.exp(-(t - T0) / K) *
                     np.sin(omega * t)) +
                    setpoint)

        T = t_rbv(T0=self._T0,
                  **{k: getattr(self, k).value
                     for k in ['setpoint', 'K', 'omega', 'Tvar']})

        setpoint = self.setpoint.value
        if np.abs(setpoint - T) > self.deadband.value:
            self._entered_band = -1
        elif self._entered_band < 0:
            self._entered_band = time.monotonic()

        if self._entered_band > 0:
            if time.monotonic() > self._entered_band + self.settle_time.value:
                if self.state.value != 'stable':
                    await self.state.write('stable')
        else:
            if self.state.value != 'settling':
                await self.state.write('settling')

        await instance.write(value=T)

    @setpoint.putter
    async def setpoint(self, instance, value):
        self._T0 = time.monotonic()
        # ensure it flashes low
        await self.state.write('stable')
        await self.state.write('settling')
        return value


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='thermo:',
        desc=dedent(Thermo.__doc__))
    ioc = Thermo(**ioc_options)
    run(ioc.pvdb, **run_options)
