from bluesky import RunEngine
import bluesky.plans as bp
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.utils import install_kicker
import matplotlib
from databroker import Broker

matplotlib.use('qt5agg')
install_kicker()


bec = BestEffortCallback()
db = Broker.named('temp')
RE = RunEngine()

RE.subscribe(bec)
RE.subscribe(db.insert)
