from ..common import I2cComponent
from ..cpld import SysCpld, SysCpldCommonRegisters

from ...accessors.fan import FanImpl
from ...accessors.led import LedImpl
from ...accessors.rook import RookLedImpl

from ...core.component import Component
from ...core.log import getLogger
from ...core.register import Register, RegBitField

from ...drivers.i2c import I2cKernelFanDriver
from ...drivers.rook import RookLedSysfsDriver
from ...drivers.sysfs import LedSysfsDriver

logging = getLogger(__name__)

class RookCpldRegisters(SysCpldCommonRegisters):
   INTERRUPT_STS = Register(0x08,
      RegBitField(0, 'scdCrcError'),
   )
   SCD_CTRL_STS = Register(0x0A,
      RegBitField(0, 'scdConfDone'),
      RegBitField(1, 'scdInitDone'),
      RegBitField(5, 'scdReset', ro=False),
   )
   PWR_CYC_EN = Register(0x17,
      RegBitField(0, 'powerCycleOnCrc', ro=False),
   )

class RookSysCpld(SysCpld):
   def __init__(self, addr, drivers=None, registerCls=RookCpldRegisters, **kwargs):
      super(RookSysCpld, self).__init__(addr=addr, drivers=drivers,
                                        registerCls=registerCls, **kwargs)

class RookLedComponent(Component):
   def __init__(self, baseName=None, scd=None, drivers=None, **kwargs):
      self.baseName = baseName
      if not drivers:
         drivers = [RookLedSysfsDriver(sysfsPath='/sys/class/leds/')]
      super(RookLedComponent, self).__init__(drivers=drivers, **kwargs)

   def createLed(self, colors=None, name=None):
      return RookLedImpl(baseName=self.baseName, colors=colors or [], name=name,
                         driver=self.drivers['RookLedSysfsDriver'])

class LAFanCpldComponent(I2cComponent):
   def __init__(self, addr=None, drivers=None, waitFile=None, **kwargs):
      if not drivers:
         fanSysfsDriver = I2cKernelFanDriver(name='la_cpld',
               module='rook-fan-cpld', addr=addr, maxPwm=255, waitFile=waitFile)
         ledSysfsDriver = LedSysfsDriver(sysfsPath='/sys/class/leds')
         drivers = [fanSysfsDriver, ledSysfsDriver]
      super(LAFanCpldComponent, self).__init__(addr=addr, drivers=drivers,
                                               **kwargs)

   def createFan(self, fanId, driver='I2cKernelFanDriver',
                 ledDriver='LedSysfsDriver', **kwargs):
      logging.debug('creating LA fan %s', fanId)
      driver = self.drivers[driver]
      led = LedImpl(name='fan%s' % fanId, driver=self.drivers[ledDriver])
      return FanImpl(fanId=fanId, driver=driver, led=led, **kwargs)

class TehamaFanCpldComponent(I2cComponent):
   def __init__(self, addr=None, drivers=None, waitFile=None, **kwargs):
      if not drivers:
         fanSysfsDriver = I2cKernelFanDriver(name='tehama_cpld',
               module='rook-fan-cpld', addr=addr, maxPwm=255, waitFile=waitFile)
         ledSysfsDriver = LedSysfsDriver(sysfsPath='/sys/class/leds')
         drivers = [fanSysfsDriver, ledSysfsDriver]
      super(TehamaFanCpldComponent, self).__init__(addr=addr, drivers=drivers,
                                                   **kwargs)

   def createFan(self, fanId, driver='I2cKernelFanDriver',
                 ledDriver='LedSysfsDriver', **kwargs):
      logging.debug('creating Tehama fan %s', fanId)
      driver = self.drivers[driver]
      led = LedImpl(name='fan%s' % fanId, driver=self.drivers[ledDriver])
      return FanImpl(fanId=fanId, driver=driver, led=led, **kwargs)

