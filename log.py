# -*- coding: utf-8 -*-

# log.py
# Logging Module

def debug_log(type, printable, backtrace=True):
   _DEBUG_ = True

   if not _DEBUG_:
      return

   _caller_trace_names = list()

   logger = __import__('sys').stdout.write
   curr_stack = __import__('inspect').stack()
   get_module = __import__('inspect').getmodule

   def _system():
      logger('[*] ')

   def _warning():
      logger('[-] ')

   def _information():
      logger('[!] ')

   def _exclamation():
      logger('[~] ')   

   _types = {  
            'system': _system,
            'warning': _warning,
            'information': _information,
            'exclamation': _exclamation
          }

   assert _types.has_key(type) == True

   _types[type]()
   logger("'%s' at line number %d\n" % (printable, curr_stack[0][0].f_back.f_lineno))

   for _stack_trace_start in xrange(len(curr_stack)-2, 0, -1):
      _parent_frame = curr_stack[_stack_trace_start][0]
      _module = get_module(_parent_frame)

      if _module and _module.__name__ not in _caller_trace_names: # Tracing a recursive function sucks!
         _caller_trace_names.append(_module.__name__)
         
      if 'self' in _parent_frame.f_locals:
         _caller_trace_names.append(_parent_frame.f_locals['self'].__class__.__name__)

      _code_name = _parent_frame.f_code.co_name
         
      if _code_name != '<module>':
         _caller_trace_names.append(_code_name)

   logger("-"*50+"\n")
   logger("<Caller Trace Logs in %s> \n" % (_parent_frame.f_code.co_filename))

   for idx, callers in enumerate(_caller_trace_names):
      logger("%s[%s]" % ("    "*idx, callers))
      
      if callers == curr_stack[1][0].f_code.co_name:
         logger(" <---- HERE YOU ARE")

      logger("\n")

   logger("-"*50+"\n")
   
if __name__ == "__main__":
   def a():
      def b():
         debug_log("information", "this is a testing log")
      b()
   a()
   
