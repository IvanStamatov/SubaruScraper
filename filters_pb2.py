# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: filters.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='filters.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\rfilters.proto\"&\n\x07\x46ilters\x12\x0c\n\x04type\x18\x01 \x03(\t\x12\r\n\x05\x62rand\x18\x02 \x03(\tb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_FILTERS = _descriptor.Descriptor(
  name='Filters',
  full_name='Filters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Filters.type', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='brand', full_name='Filters.brand', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=55,
)

DESCRIPTOR.message_types_by_name['Filters'] = _FILTERS

Filters = _reflection.GeneratedProtocolMessageType('Filters', (_message.Message,), dict(
  DESCRIPTOR = _FILTERS,
  __module__ = 'filters_pb2'
  # @@protoc_insertion_point(class_scope:Filters)
  ))
_sym_db.RegisterMessage(Filters)


# @@protoc_insertion_point(module_scope)
