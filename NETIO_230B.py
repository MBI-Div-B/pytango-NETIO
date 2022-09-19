# -*- coding: utf-8 -*-
#
# This file is part of the NETIO_230B project
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

""" 

"""

# PyTango imports
from encodings import utf_8
import tango
from tango import DebugIt
from tango.server import run
from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState,Attr, WAttribute
from tango import AttrWriteType, PipeWriteType

# Additional import
# PROTECTED REGION ID(NETIO_230B.additionnal_import) ENABLED START #
from enum import IntEnum
from telnetlib import Telnet

class socket_state(IntEnum):
    OFF = 0
    ON = 1
# PROTECTED REGION END #    //  NETIO_230B.additionnal_import

__all__ = ["NETIO_230B", "main"]


class NETIO_230B(Device):
    """

    **Properties:**

    - Class Property
        username
            - Type:'DevString'
        password
            - Type:'DevString'
        ipadress
            - Type:'DevString'
        port
            - Type:'DevString'
    """
    # PROTECTED REGION ID(NETIO_230B.class_variable) ENABLED START #
    def read_socket(self, attr):
        """Reads the state of the Socket attr"""
        self.tn.write(bytes('port {}\n'.format(attr.get_name()[6:]),'utf-8'))
        #self.tn.msg(b'check1')
        ret = str(self.tn.read_until(b'check1', timeout=0.1))
        attr.set_value(bool(int(ret[-6])))
        return bool(int(ret[-6]))
        
        

    def write_socket(self,attr):
        value = bool(attr.get_write_value())
        self.info_stream(str(attr.get_write_value))
        self.info_stream("Writting attribute %s", attr.get_name())
        self.tn.write(bytes('port {} {}\n'.format(attr.get_name()[6:],int(value)),'utf-8'))
        attr.set_value(value)
    # PROTECTED REGION END #    //  NETIO_230B.class_variable

    # ----------------
    # Class Properties
    # ----------------

    username = device_property(
        dtype='DevString',
        default_value="admin"
    )

    password = device_property(
        dtype='DevString',
        default_value="admin"
    )

    ipaddress = device_property(
        dtype='DevString',
    )

    port = device_property(
        dtype='DevString',
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        """Initialises the attributes and properties of the NETIO_230B."""
        Device.init_device(self)
        # PROTECTED REGION ID(NETIO_230B.init_device) ENABLED START #
        self.tn = Telnet()
        self.tn.open(self.ipaddress, port=self.port , timeout=1)
        self.tn.write(bytes('login ' + self.username + ' ' + self.password + '\n','utf-8'))
        self.tn.write(b'port list\n')
        self.tn.msg(b'check1')
        ret = self.tn.read_until(b'check1', timeout=1)
        #self.info_stream(ret)
        ret = str(ret)
        ret = ret.split(' ')[-1]
        #self.info_stream(str(len(ret)+1))
        for i in range(len(ret)-5):
            self.create_enum_attributes('socket'+str(i+1))
        #self.tn.write(bytes('port list 0000', 'utf-8'))
        #self.info_stream(str(self.read_socket(socket1)))

        # PROTECTED REGION END #    //  NETIO_230B.init_device

    def always_executed_hook(self):
        """Method always executed before any TANGO command is executed."""
        # PROTECTED REGION ID(NETIO_230B.always_executed_hook) ENABLED START #

        # PROTECTED REGION END #    //  NETIO_230B.always_executed_hook

    def delete_device(self):
        """Hook to delete resources allocated in init_device.

        This method allows for any memory or other resources allocated in the
        init_device method to be released.  This method is called by the device
        destructor and by the device Init command.
        """
        # PROTECTED REGION ID(NETIO_230B.delete_device) ENABLED START #
        self.tn.close()
        # PROTECTED REGION END #    //  NETIO_230B.delete_device
    # --------
    # Commands
    # --------

    @command(
        dtype_in='DevString',
        doc_in="dev_name",
        display_level=DispLevel.EXPERT,
    )
    @DebugIt()
    def create_enum_attributes(self, argin):
        # PROTECTED REGION ID(NETIO_230B.create_enum_attributes) ENABLED START #
        """
        Command creates a new Enum Attribute

        :param argin: 'DevString'
        dev_name

        :return:None
        """
        attr = attribute(
            name=argin,
            dtype=socket_state,
            access=AttrWriteType.READ_WRITE,
            label=argin,
        ).to_attr()
        self.add_attribute(attr,r_meth=self.read_socket,w_meth=self.write_socket)
        # PROTECTED REGION END #    //  NETIO_230B.create_enum_attributes

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    """Main function of the NETIO_230B module."""
    # PROTECTED REGION ID(NETIO_230B.main) ENABLED START #
    return run((NETIO_230B,), args=args, **kwargs)
    # PROTECTED REGION END #    //  NETIO_230B.main


if __name__ == '__main__':
    main()
