# Required Imports
import google.protobuf.text_format as tf

# Google Protocol Buffer
import examples.grammar_argos.proto.tutorial_pb2 as pb

person = pb.Person()
person.id = 1234
person.name = "Troy"
person.email = "zivia@unm.edu"
print type(person.phone)
print 'Directory' + str(dir(person.phone._message_descriptor.fields))
phone = person.phone.add()
phone.number = "414-5379"
phone.type = pb.Person.HOME


print '\nGenerated Message\n'
print tf.MessageToString(person)
