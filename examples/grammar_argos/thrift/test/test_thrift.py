import thriftpy
foraging_thrift = thriftpy.load("../foraging.thrift", module_name="foraging_thrift")

print foraging_thrift
print dir(foraging_thrift)
print foraging_thrift.Root
root = foraging_thrift.Root()
print root
root.init = foraging_thrift.StateInitialize
print root