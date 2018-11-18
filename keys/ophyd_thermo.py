import ophyd
from ophyd import Component as Cpt, EpicsSignal, EpicsSignalRO, DeviceStatus
from typhon import TyphonSuite
from qtpy import QtWidgets

app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication([b"python epics"])


class ThermoDevice(ophyd.Device):
    readback = Cpt(EpicsSignalRO, 'I')
    setpoint = Cpt(EpicsSignal, 'SP')
    k = Cpt(EpicsSignal, 'K', kind='config')
    omega = Cpt(EpicsSignal, 'omega', kind='config')
    tvar = Cpt(EpicsSignal, 'Tvar', kind='config')
    state = Cpt(EpicsSignalRO, 'state', string=True)
    deadband = Cpt(EpicsSignal, 'deadband', kind='config')
    settle_time = Cpt(EpicsSignal, 'settle_time', kind='config')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._status = None
        self.state.subscribe(self._state_change)

    def _state_change(self, old_value, value, **kwargs):
        st = self._status
        # TODO handle the enum better
        # TODO it is possible to get race-conditions in here :(
        if int(old_value) == 1 and int(value) == 0 and st is not None:
            self._status = None
            st._finished()

    def set(self, val):
        st = self._status
        if st is not None:
            st._finished(success=False)
            self._status = None

        self._status = DeviceStatus(self)
        self.setpoint.put(val)
        return self._status


td = ThermoDevice('thermo:', name='td')
suite = TyphonSuite.from_device(td)
suite.show()
