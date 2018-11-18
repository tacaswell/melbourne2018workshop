import ophyd
from ophyd import Component as Cpt, EpicsSignal, EpicsSignalRO, DeviceStatus
from typhon import TyphonSuite
from qtpy import QtWidgets


class PointDetectorDevice(ophyd.Device):
    mtr = Cpt(EpicsSignal, 'mtr')
    exp = Cpt(EpicsSignal, 'exp', kind='config')
    det = Cpt(EpicsSignalRO, 'det')
    acq = Cpt(EpicsSignal, 'acq', kind='omitted')
    busy = Cpt(EpicsSignalRO, 'busy', kind='omitted')

    def trigger(self):
        st = DeviceStatus(self)
        self.acq.put(1, callback=st._finished)
        return st


# this is to make sure typhon does not crash out
app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication([b"python epics"])

pd = PointDetectorDevice('point:', name='pd')
point_suite = TyphonSuite.from_device(pd)
point_suite.show()
