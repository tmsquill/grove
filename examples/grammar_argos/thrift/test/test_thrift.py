import thriftpy

foraging_thrift = thriftpy.load("../foraging.thrift", module_name="foraging_thrift")

print foraging_thrift
print dir(foraging_thrift)
print foraging_thrift.Root
root = foraging_thrift.Root()
print root
root.init = foraging_thrift.StateInitialize()
print root
print dir(root.init)
print root.init.thrift_spec
print root.init.default_spec
root.init.init_2 = foraging_thrift.ProbInitState.PROB_INIT_STATE_0
print root.init.thrift_spec
print root.init.default_spec
print root.init.init_2

import thriftpy.transport as tran
import thriftpy.protocol as prot

transOut = tran.TMemoryBuffer()
protocolOut = prot.TBinaryProtocol(transOut)
root.write(protocolOut)
print transOut.getvalue()