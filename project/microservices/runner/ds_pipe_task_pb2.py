# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ds_pipe_task.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ds_pipe_task.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12\x64s_pipe_task.proto\"\xdc\x01\n\x04Task\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x11\n\talgorithm\x18\x02 \x01(\t\x12\x19\n\x11number_of_samples\x18\x03 \x01(\x05\x12\x14\n\x0c\x64\x61taset_name\x18\x04 \x01(\t\x12\x13\n\x0bn_neighbors\x18\x05 \x01(\x05\x12\x17\n\x0fquality_measure\x18\x06 \x01(\t\x12\x18\n\x10percent_labelled\x18\x07 \x01(\x02\x12\r\n\x05\x61lpha\x18\x08 \x01(\x02\x12\r\n\x05gamma\x18\t \x01(\x02\x12\x19\n\x11\x65valuation_method\x18\n \x01(\t\";\n\x0eResult_Request\x12\x11\n\tresult_id\x18\x01 \x01(\x05\x12\x16\n\x0e\x61lgorithm_name\x18\x02 \x01(\t\"*\n\x14Has_Results_Response\x12\x12\n\nhas_result\x18\x01 \x01(\x08\"\x1f\n\x0cTask_Results\x12\x0f\n\x07results\x18\x01 \x03(\x02\x32*\n\x06Runner\x12 \n\x08Run_task\x12\x05.Task\x1a\r.Task_Results2\xa2\x01\n\x0eTask_Evaluator\x12-\n\rEvaluate_Task\x12\x05.Task\x1a\x15.Has_Results_Response\x12\x30\n\x0eResultResponse\x12\x0f.Result_Request\x1a\r.Task_Results\x12/\n\x15\x43onfigurationResponse\x12\x0f.Result_Request\x1a\x05.Taskb\x06proto3'
)




_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_id', full_name='Task.user_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='algorithm', full_name='Task.algorithm', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='number_of_samples', full_name='Task.number_of_samples', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dataset_name', full_name='Task.dataset_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='n_neighbors', full_name='Task.n_neighbors', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='quality_measure', full_name='Task.quality_measure', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='percent_labelled', full_name='Task.percent_labelled', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='alpha', full_name='Task.alpha', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gamma', full_name='Task.gamma', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='evaluation_method', full_name='Task.evaluation_method', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=243,
)


_RESULT_REQUEST = _descriptor.Descriptor(
  name='Result_Request',
  full_name='Result_Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result_id', full_name='Result_Request.result_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='algorithm_name', full_name='Result_Request.algorithm_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=245,
  serialized_end=304,
)


_HAS_RESULTS_RESPONSE = _descriptor.Descriptor(
  name='Has_Results_Response',
  full_name='Has_Results_Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='has_result', full_name='Has_Results_Response.has_result', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=306,
  serialized_end=348,
)


_TASK_RESULTS = _descriptor.Descriptor(
  name='Task_Results',
  full_name='Task_Results',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='Task_Results.results', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=350,
  serialized_end=381,
)

DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['Result_Request'] = _RESULT_REQUEST
DESCRIPTOR.message_types_by_name['Has_Results_Response'] = _HAS_RESULTS_RESPONSE
DESCRIPTOR.message_types_by_name['Task_Results'] = _TASK_RESULTS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'ds_pipe_task_pb2'
  # @@protoc_insertion_point(class_scope:Task)
  })
_sym_db.RegisterMessage(Task)

Result_Request = _reflection.GeneratedProtocolMessageType('Result_Request', (_message.Message,), {
  'DESCRIPTOR' : _RESULT_REQUEST,
  '__module__' : 'ds_pipe_task_pb2'
  # @@protoc_insertion_point(class_scope:Result_Request)
  })
_sym_db.RegisterMessage(Result_Request)

Has_Results_Response = _reflection.GeneratedProtocolMessageType('Has_Results_Response', (_message.Message,), {
  'DESCRIPTOR' : _HAS_RESULTS_RESPONSE,
  '__module__' : 'ds_pipe_task_pb2'
  # @@protoc_insertion_point(class_scope:Has_Results_Response)
  })
_sym_db.RegisterMessage(Has_Results_Response)

Task_Results = _reflection.GeneratedProtocolMessageType('Task_Results', (_message.Message,), {
  'DESCRIPTOR' : _TASK_RESULTS,
  '__module__' : 'ds_pipe_task_pb2'
  # @@protoc_insertion_point(class_scope:Task_Results)
  })
_sym_db.RegisterMessage(Task_Results)



_RUNNER = _descriptor.ServiceDescriptor(
  name='Runner',
  full_name='Runner',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=383,
  serialized_end=425,
  methods=[
  _descriptor.MethodDescriptor(
    name='Run_task',
    full_name='Runner.Run_task',
    index=0,
    containing_service=None,
    input_type=_TASK,
    output_type=_TASK_RESULTS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_RUNNER)

DESCRIPTOR.services_by_name['Runner'] = _RUNNER


_TASK_EVALUATOR = _descriptor.ServiceDescriptor(
  name='Task_Evaluator',
  full_name='Task_Evaluator',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=428,
  serialized_end=590,
  methods=[
  _descriptor.MethodDescriptor(
    name='Evaluate_Task',
    full_name='Task_Evaluator.Evaluate_Task',
    index=0,
    containing_service=None,
    input_type=_TASK,
    output_type=_HAS_RESULTS_RESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ResultResponse',
    full_name='Task_Evaluator.ResultResponse',
    index=1,
    containing_service=None,
    input_type=_RESULT_REQUEST,
    output_type=_TASK_RESULTS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ConfigurationResponse',
    full_name='Task_Evaluator.ConfigurationResponse',
    index=2,
    containing_service=None,
    input_type=_RESULT_REQUEST,
    output_type=_TASK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TASK_EVALUATOR)

DESCRIPTOR.services_by_name['Task_Evaluator'] = _TASK_EVALUATOR

# @@protoc_insertion_point(module_scope)
