from ophyd import Component as Cpt, EpicsSignal, Device


class SimpleDevice(Device):
    a = Cpt(EpicsSignal, 'A')
    b = Cpt(EpicsSignal, 'B')


class BiggerDevice(Device):
    one = Cpt(SimpleDevice, 'one:')
    two = Cpt(SimpleDevice, 'two:')

simple = SimpleDevice(prefix='simple:', name='simple')  # noqa
