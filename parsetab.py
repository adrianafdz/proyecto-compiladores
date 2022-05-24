
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "startCALL COMP DEF DO ELSE END FOR FUNC ID IF INPUT MAIN NOTHING NUM NUMBER OPFACT OPTERM PRINT PROGRAM RET STR STRING THEN TO TO_NUMBER TO_STRING TYPE WHILEstart : PROGRAM f_start ID f_prog ';' clases vars funciones MAIN f_main '(' ')' '{' estatutos '}' END f_end ';' f_start :f_prog :f_main :f_end : clases : clases clase\n              | emptyclase : TYPE ID f_startclass ':' ID f_clasepadre '{' cvars f_cvars funciones '}' f_endclass \n             | TYPE ID f_startclass '{' cvars f_cvars funciones '}' f_endclass f_startclass :f_clasepadre :f_cvars :f_endclass :funciones : funciones funcion\n                  | emptyfuncion : FUNC ID f_startfunc '(' params ')' ':' tipo f_tipofunc '{' vars estatutos '}' f_endfunc\n               | FUNC ID f_startfunc '(' params ')' ':' NOTHING f_nothing f_tipofunc '{' vars estatutos '}' f_endfunc f_startfunc :f_nothing :f_tipofunc :f_endfunc :vars : vars DEF tipo dimension ':' lista_id ';'\n            | vars DEF ID f_varsobj ':' lista_id_obj ';'\n            | emptyf_varsobj :cvars : cvars DEF tipo dimension ':' lista_id_in_obj ';'\n             | emptylista_id_in_obj : ID f_vars_in_obj\n                       | lista_id_in_obj ',' ID f_vars_in_objf_vars_in_obj :lista_id : ID f_vars\n                | lista_id ',' ID f_varsf_vars :lista_id_obj : ID f_vars_obj\n                    | lista_id_obj ',' ID f_vars_objf_vars_obj :dimension : '[' NUM f_dim1 ']' f_onedim\n                 | '[' NUM f_dim1 ']' '[' NUM f_dim2 ']' f_twodim\n                 | emptyf_dim1 :f_dim2 :f_onedim :f_twodim :tipo : NUMBER \n            | STRINGparams : pparams \n              | emptypparams : tipo ID f_param\n               | pparams ',' tipo ID f_paramf_param :estatutos : estatutos estatuto \n                 | emptyestatuto : asignacion \n                | while \n                | for \n                | condicion \n                | CALL call_func ';' call_func : func\n                 | input \n                 | write \n                 | to_num \n                 | to_str\n                 | return func : ID  f_verify_func '(' args ')'\n            | ID  f_varobj ':' ID f_verify_func_composite '(' args ')' f_verify_func :f_verify_func_composite :args : args_list f_end_args\n            | f_end_argsargs_list : expresion f_arg\n                 | args_list ',' expresion f_argf_arg :f_end_args :asignacion : var '=' f_oper expresion ';' var : ID f_varobj ':' ID f_verify_type_composite indexacion\n           | ID f_verify_type indexacionindexacion : f_start_array '[' expresion f_index ']' f_end_array\n                 | f_start_array '[' expresion f_index ']' '[' f_next_index expresion f_index ']' f_end_array\n                 | f_no_index emptyf_varobj :f_verify_type :f_verify_type_composite :f_no_index :f_start_array :f_index :f_next_index :f_end_array :expresion : exp\n                 | expresion COMP f_oper exp f_expresf_expres :exp : term\n           | exp OPTERM f_oper term f_expf_exp :term : fact\n            | term OPFACT f_oper fact f_termf_term :f_oper :fact : '(' lparen expresion ')' rparen\n            | var\n            | NUM f_fact\n            | OPTERM NUM\n            | CALL call_func f_return_val f_return_val :lparen :rparen :f_fact :condicion : IF '(' expresion ')' f_if THEN '{' estatutos '}' condicionp f_endifcondicionp : ELSE f_else '{' estatutos '}'\n                  | empty f_if :f_endif :f_else :while : WHILE f_while '(' expresion f_exprwhile ')' DO '{' estatutos '}' f_endwhile f_while :f_exprwhile :f_endwhile :for : FOR expresion f_for_start TO expresion f_for_to '{' estatutos '}' f_for_end f_for_start :f_for_to :f_for_end :to_num : TO_NUMBER '(' STR ')' \n              | TO_NUMBER '(' var ')' to_str : TO_STRING '(' expresion ')' input : INPUT '(' var ')' write : PRINT '(' write_list ')' write_list : write_list '&' write_listp\n                  | write_listpwrite_listp : STR \n                   | var \n                   | CALL to_strreturn : RET '(' expresion ')' empty :"
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,169,],[0,-1,]),'ID':([2,3,11,12,14,19,22,23,31,35,37,51,53,56,57,61,62,66,67,80,81,82,83,84,85,88,92,98,115,122,125,126,134,139,142,143,144,145,146,147,148,150,151,152,154,164,167,170,171,184,185,186,187,191,205,211,219,220,226,237,238,241,243,244,246,247,251,252,253,256,258,259,260,263,264,265,267,269,270,273,275,276,],[-2,4,-24,16,21,26,-44,-45,38,44,46,-132,69,-22,71,-23,74,78,-52,-51,-53,-54,-55,-56,109,78,129,133,-97,-104,109,78,166,-57,78,78,78,78,78,78,78,-97,-97,-97,78,195,78,78,202,78,78,78,78,-132,78,-74,-132,-132,78,78,-132,78,-132,-132,78,-86,-132,78,78,78,78,-120,-132,-116,-117,-111,-109,-113,-107,-132,78,-108,]),';':([4,5,43,44,46,47,58,60,71,74,78,93,95,100,101,102,103,104,105,106,107,108,118,119,121,123,124,132,133,135,137,138,153,155,156,165,166,168,182,189,195,196,203,204,207,208,209,210,214,215,216,217,221,222,224,232,233,234,235,239,248,257,272,274,],[-3,6,56,-33,-36,61,-31,-34,-33,-36,-81,-32,-35,-83,-5,139,-58,-59,-60,-61,-62,-63,-88,-91,-94,-99,-106,163,-30,-76,-132,169,-101,-100,-103,-28,-82,-79,211,-102,-30,-83,-124,-125,-121,-122,-123,-131,-90,-93,-96,-105,-29,-75,-64,-89,-92,-95,-98,-87,-77,-65,-87,-78,]),'TYPE':([6,7,8,10,76,97,162,194,],[-132,12,-7,-6,-13,-9,-13,-8,]),'DEF':([6,7,8,9,10,11,32,39,40,56,61,63,75,76,97,162,163,191,194,219,220,238,],[-132,-132,-7,14,-6,-24,-132,50,-27,-22,-23,-132,50,-13,-9,-13,-26,-132,-8,14,-132,14,]),'MAIN':([6,7,8,9,10,11,13,15,18,56,61,76,97,162,194,245,254,255,261,],[-132,-132,-7,-132,-6,-24,17,-15,-14,-22,-23,-13,-9,-13,-8,-21,-16,-21,-17,]),'FUNC':([6,7,8,9,10,11,13,15,18,32,39,40,49,56,61,63,64,75,76,96,97,131,162,163,194,245,254,255,261,],[-132,-132,-7,-132,-6,-24,19,-15,-14,-132,-12,-27,-132,-22,-23,-132,19,-12,-13,-132,-9,19,-13,-26,-8,-21,-16,-21,-17,]),'}':([11,15,18,32,39,40,49,51,56,61,63,64,66,67,75,80,81,82,83,84,96,131,139,163,191,211,219,220,237,238,243,244,245,246,251,252,253,254,255,258,259,260,261,263,264,265,267,269,270,273,275,276,],[-24,-15,-14,-132,-12,-27,-132,-132,-22,-23,-132,76,79,-52,-12,-51,-53,-54,-55,-56,-132,162,-57,-26,-132,-74,-132,-132,245,-132,-132,-132,-21,255,-132,259,260,-16,-21,263,-120,-132,-17,-116,-117,-111,-109,-113,-107,-132,276,-108,]),'CALL':([11,51,56,61,66,67,80,81,82,83,84,88,115,122,126,139,143,145,146,147,148,150,151,152,154,167,170,184,185,186,187,191,205,211,219,220,226,237,238,241,243,244,246,247,251,252,253,256,258,259,260,263,264,265,267,269,270,273,275,276,],[-24,-132,-22,-23,85,-52,-51,-53,-54,-55,-56,125,-97,-104,125,-57,177,125,125,125,125,-97,-97,-97,125,125,125,125,125,125,125,-132,177,-74,-132,-132,125,85,-132,125,-132,-132,85,-86,-132,85,85,125,85,-120,-132,-116,-117,-111,-109,-113,-107,-132,85,-108,]),'WHILE':([11,51,56,61,66,67,80,81,82,83,84,139,191,211,219,220,237,238,243,244,246,251,252,253,258,259,260,263,264,265,267,269,270,273,275,276,],[-24,-132,-22,-23,87,-52,-51,-53,-54,-55,-56,-57,-132,-74,-132,-132,87,-132,-132,-132,87,-132,87,87,87,-120,-132,-116,-117,-111,-109,-113,-107,-132,87,-108,]),'FOR':([11,51,56,61,66,67,80,81,82,83,84,139,191,211,219,220,237,238,243,244,246,251,252,253,258,259,260,263,264,265,267,269,270,273,275,276,],[-24,-132,-22,-23,88,-52,-51,-53,-54,-55,-56,-57,-132,-74,-132,-132,88,-132,-132,-132,88,-132,88,88,88,-120,-132,-116,-117,-111,-109,-113,-107,-132,88,-108,]),'IF':([11,51,56,61,66,67,80,81,82,83,84,139,191,211,219,220,237,238,243,244,246,251,252,253,258,259,260,263,264,265,267,269,270,273,275,276,],[-24,-132,-22,-23,89,-52,-51,-53,-54,-55,-56,-57,-132,-74,-132,-132,89,-132,-132,-132,89,-132,89,89,89,-120,-132,-116,-117,-111,-109,-113,-107,-132,89,-108,]),'NUMBER':([14,42,50,70,90,],[22,22,22,22,22,]),'STRING':([14,42,50,70,90,],[23,23,23,23,23,]),':':([16,20,21,22,23,24,27,29,30,59,65,68,73,77,78,99,109,141,161,193,],[-10,-132,-25,-44,-45,31,35,-39,37,-42,-132,90,-37,98,-80,134,-80,171,-43,-38,]),'{':([16,22,23,24,38,41,48,78,100,103,104,105,106,107,108,118,119,121,123,124,127,128,135,137,153,155,156,158,159,166,168,189,192,196,203,204,207,208,209,210,213,214,215,216,217,222,224,231,232,233,234,235,236,239,242,248,257,266,271,272,274,],[-10,-44,-45,32,-11,51,63,-81,-83,-58,-59,-60,-61,-62,-63,-88,-91,-94,-99,-106,-20,-19,-76,-132,-101,-100,-103,191,-20,-82,-79,-102,220,-83,-124,-125,-121,-122,-123,-131,-119,-90,-93,-96,-105,-75,-64,243,-89,-92,-95,-98,244,-87,251,-77,-65,-112,273,-87,-78,]),'(':([17,25,26,34,87,88,89,109,110,111,112,113,114,115,116,122,126,140,145,146,147,148,150,151,152,154,167,170,184,185,186,187,202,226,228,241,247,256,],[-4,33,-18,42,-114,122,126,-66,142,143,144,145,146,-97,148,-104,122,170,122,122,122,122,-97,-97,-97,122,122,122,122,122,122,122,-67,122,241,122,-86,122,]),'[':([20,22,23,59,65,78,100,136,166,196,239,],[28,-44,-45,72,28,-81,-84,167,-82,-84,247,]),'NUM':([28,72,88,115,120,122,126,145,146,147,148,150,151,152,154,167,170,184,185,186,187,226,241,247,256,],[36,94,124,-97,153,-104,124,124,124,124,124,-97,-97,-97,124,124,124,124,124,124,124,124,124,-86,124,]),')':([33,42,52,54,55,69,78,91,100,103,104,105,106,107,108,118,119,121,123,124,129,135,137,153,155,156,157,160,166,168,170,172,173,174,175,176,178,179,180,181,183,188,189,196,198,199,200,201,203,204,206,207,208,209,210,212,214,215,216,217,222,224,225,227,229,232,233,234,235,239,240,241,248,249,250,257,272,274,],[41,-132,68,-46,-47,-50,-81,-48,-83,-58,-59,-60,-61,-62,-63,-88,-91,-94,-99,-106,-50,-76,-132,-101,-100,-103,190,-49,-82,-79,-73,203,204,-127,-128,-129,207,208,209,210,-115,217,-102,-83,224,-73,-69,-72,-124,-125,-130,-121,-122,-123,-131,230,-90,-93,-96,-105,-75,-64,-68,-70,-126,-89,-92,-95,-98,-87,-72,-73,-77,-71,257,-65,-87,-78,]),']':([36,45,78,94,100,103,104,105,106,107,108,118,119,121,123,124,130,135,137,153,155,156,166,168,189,196,197,203,204,207,208,209,210,214,215,216,217,222,223,224,232,233,234,235,239,248,257,262,268,272,274,],[-40,59,-81,-41,-83,-58,-59,-60,-61,-62,-63,-88,-91,-94,-99,-106,161,-76,-132,-101,-100,-103,-82,-79,-102,-83,-85,-124,-125,-121,-122,-123,-131,-90,-93,-96,-105,-75,239,-64,-89,-92,-95,-98,-87,-77,-65,-85,272,-87,-78,]),',':([43,44,46,47,54,58,60,69,71,74,78,91,93,95,100,103,104,105,106,107,108,118,119,121,123,124,129,132,133,135,137,153,155,156,160,165,166,168,189,195,196,199,201,203,204,207,208,209,210,214,215,216,217,221,222,224,227,232,233,234,235,239,240,248,249,257,272,274,],[57,-33,-36,62,70,-31,-34,-50,-33,-36,-81,-48,-32,-35,-83,-58,-59,-60,-61,-62,-63,-88,-91,-94,-99,-106,-50,164,-30,-76,-132,-101,-100,-103,-49,-28,-82,-79,-102,-30,-83,226,-72,-124,-125,-121,-122,-123,-131,-90,-93,-96,-105,-29,-75,-64,-70,-89,-92,-95,-98,-87,-72,-77,-71,-65,-87,-78,]),'=':([78,86,100,135,137,166,168,196,222,239,248,272,274,],[-81,115,-83,-76,-132,-82,-79,-83,-75,-87,-77,-87,-78,]),'OPFACT':([78,100,103,104,105,106,107,108,119,121,123,124,135,137,153,155,156,166,168,189,196,203,204,207,208,209,210,215,216,217,222,224,234,235,239,248,257,272,274,],[-81,-83,-58,-59,-60,-61,-62,-63,152,-94,-99,-106,-76,-132,-101,-100,-103,-82,-79,-102,-83,-124,-125,-121,-122,-123,-131,152,-96,-105,-75,-64,-95,-98,-87,-77,-65,-87,-78,]),'OPTERM':([78,88,100,103,104,105,106,107,108,115,118,119,121,122,123,124,126,135,137,145,146,147,148,150,151,152,153,154,155,156,166,167,168,170,184,185,186,187,189,196,203,204,207,208,209,210,214,215,216,217,222,224,226,233,234,235,239,241,247,248,256,257,272,274,],[-81,120,-83,-58,-59,-60,-61,-62,-63,-97,151,-91,-94,-104,-99,-106,120,-76,-132,120,120,120,120,-97,-97,-97,-101,120,-100,-103,-82,120,-79,120,120,120,120,120,-102,-83,-124,-125,-121,-122,-123,-131,151,-93,-96,-105,-75,-64,120,-92,-95,-98,-87,120,-86,-77,120,-65,-87,-78,]),'COMP':([78,100,103,104,105,106,107,108,117,118,119,121,123,124,135,137,153,155,156,157,166,168,180,181,182,183,188,189,196,197,201,203,204,207,208,209,210,213,214,215,216,217,222,224,232,233,234,235,239,240,248,257,262,272,274,],[-81,-83,-58,-59,-60,-61,-62,-63,150,-88,-91,-94,-99,-106,-76,-132,-101,-100,-103,150,-82,-79,150,150,150,150,150,-102,-83,150,150,-124,-125,-121,-122,-123,-131,150,-90,-93,-96,-105,-75,-64,-89,-92,-95,-98,-87,150,-77,-65,150,-87,-78,]),'TO':([78,100,103,104,105,106,107,108,117,118,119,121,123,124,135,137,149,153,155,156,166,168,189,196,203,204,207,208,209,210,214,215,216,217,222,224,232,233,234,235,239,248,257,272,274,],[-81,-83,-58,-59,-60,-61,-62,-63,-118,-88,-91,-94,-99,-106,-76,-132,184,-101,-100,-103,-82,-79,-102,-83,-124,-125,-121,-122,-123,-131,-90,-93,-96,-105,-75,-64,-89,-92,-95,-98,-87,-77,-65,-87,-78,]),'&':([78,100,135,137,166,168,173,174,175,176,196,206,209,222,229,239,248,272,274,],[-81,-83,-76,-132,-82,-79,205,-127,-128,-129,-83,-130,-123,-75,-126,-87,-77,-87,-78,]),'END':([79,],[101,]),'INPUT':([85,125,],[110,110,]),'PRINT':([85,125,],[111,111,]),'TO_NUMBER':([85,125,],[112,112,]),'TO_STRING':([85,125,177,],[113,113,113,]),'RET':([85,125,],[114,114,]),'NOTHING':([90,],[128,]),'STR':([143,144,205,],[175,178,175,]),'THEN':([190,218,],[-110,236,]),'DO':([230,],[242,]),'ELSE':([260,],[266,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'f_start':([2,],[3,]),'f_prog':([4,],[5,]),'clases':([6,],[7,]),'empty':([6,7,9,20,32,42,49,51,63,65,96,137,191,219,220,238,243,244,251,260,273,],[8,11,15,29,40,55,15,67,40,29,15,168,11,67,11,67,67,67,67,267,67,]),'vars':([7,191,220,],[9,219,238,]),'clase':([7,],[10,]),'funciones':([9,49,96,],[13,64,131,]),'funcion':([13,64,131,],[18,18,18,]),'tipo':([14,42,50,70,90,],[20,53,65,92,127,]),'f_startclass':([16,],[24,]),'f_main':([17,],[25,]),'dimension':([20,65,],[27,77,]),'f_varsobj':([21,],[30,]),'f_startfunc':([26,],[34,]),'cvars':([32,63,],[39,75,]),'lista_id':([35,],[43,]),'f_dim1':([36,],[45,]),'lista_id_obj':([37,],[47,]),'f_clasepadre':([38,],[48,]),'f_cvars':([39,75,],[49,96,]),'params':([42,],[52,]),'pparams':([42,],[54,]),'f_vars':([44,71,],[58,93,]),'f_vars_obj':([46,74,],[60,95,]),'estatutos':([51,219,238,243,244,251,273,],[66,237,246,252,253,258,275,]),'f_onedim':([59,],[73,]),'estatuto':([66,237,246,252,253,258,275,],[80,80,80,80,80,80,80,]),'asignacion':([66,237,246,252,253,258,275,],[81,81,81,81,81,81,81,]),'while':([66,237,246,252,253,258,275,],[82,82,82,82,82,82,82,]),'for':([66,237,246,252,253,258,275,],[83,83,83,83,83,83,83,]),'condicion':([66,237,246,252,253,258,275,],[84,84,84,84,84,84,84,]),'var':([66,88,126,142,143,144,145,146,147,148,154,167,170,184,185,186,187,205,226,237,241,246,252,253,256,258,275,],[86,123,123,172,176,179,123,123,123,123,123,123,123,123,123,123,123,176,123,86,123,86,86,86,123,86,86,]),'f_param':([69,129,],[91,160,]),'f_endclass':([76,162,],[97,194,]),'f_varobj':([78,109,],[99,141,]),'f_verify_type':([78,],[100,]),'call_func':([85,125,],[102,156,]),'func':([85,125,],[103,103,]),'input':([85,125,],[104,104,]),'write':([85,125,],[105,105,]),'to_num':([85,125,],[106,106,]),'to_str':([85,125,177,],[107,107,206,]),'return':([85,125,],[108,108,]),'f_while':([87,],[116,]),'expresion':([88,126,145,146,147,148,154,167,170,184,226,241,256,],[117,157,180,181,182,183,188,197,201,213,240,201,262,]),'exp':([88,126,145,146,147,148,154,167,170,184,185,226,241,256,],[118,118,118,118,118,118,118,118,118,118,214,118,118,118,]),'term':([88,126,145,146,147,148,154,167,170,184,185,186,226,241,256,],[119,119,119,119,119,119,119,119,119,119,119,215,119,119,119,]),'fact':([88,126,145,146,147,148,154,167,170,184,185,186,187,226,241,256,],[121,121,121,121,121,121,121,121,121,121,121,121,216,121,121,121,]),'f_dim2':([94,],[130,]),'lista_id_in_obj':([98,],[132,]),'indexacion':([100,196,],[135,222,]),'f_start_array':([100,196,],[136,136,]),'f_no_index':([100,196,],[137,137,]),'f_end':([101,],[138,]),'f_verify_func':([109,],[140,]),'f_oper':([115,150,151,152,],[147,185,186,187,]),'f_for_start':([117,],[149,]),'lparen':([122,],[154,]),'f_fact':([124,],[155,]),'f_tipofunc':([127,159,],[158,192,]),'f_nothing':([128,],[159,]),'f_vars_in_obj':([133,195,],[165,221,]),'write_list':([143,],[173,]),'write_listp':([143,205,],[174,229,]),'f_return_val':([156,],[189,]),'f_twodim':([161,],[193,]),'f_verify_type_composite':([166,],[196,]),'args':([170,241,],[198,250,]),'args_list':([170,241,],[199,199,]),'f_end_args':([170,199,241,],[200,225,200,]),'f_exprwhile':([183,],[212,]),'f_if':([190,],[218,]),'f_index':([197,262,],[223,268,]),'f_arg':([201,240,],[227,249,]),'f_verify_func_composite':([202,],[228,]),'f_for_to':([213,],[231,]),'f_expres':([214,],[232,]),'f_exp':([215,],[233,]),'f_term':([216,],[234,]),'rparen':([217,],[235,]),'f_end_array':([239,272,],[248,274,]),'f_endfunc':([245,255,],[254,261,]),'f_next_index':([247,],[256,]),'f_for_end':([259,],[264,]),'condicionp':([260,],[265,]),'f_endwhile':([263,],[269,]),'f_endif':([265,],[270,]),'f_else':([266,],[271,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> PROGRAM f_start ID f_prog ; clases vars funciones MAIN f_main ( ) { estatutos } END f_end ;','start',18,'p_start','aloop.py',201),
  ('f_start -> <empty>','f_start',0,'p_f_start','aloop.py',204),
  ('f_prog -> <empty>','f_prog',0,'p_f_prog','aloop.py',212),
  ('f_main -> <empty>','f_main',0,'p_f_main','aloop.py',217),
  ('f_end -> <empty>','f_end',0,'p_f_end','aloop.py',221),
  ('clases -> clases clase','clases',2,'p_clases','aloop.py',235),
  ('clases -> empty','clases',1,'p_clases','aloop.py',236),
  ('clase -> TYPE ID f_startclass : ID f_clasepadre { cvars f_cvars funciones } f_endclass','clase',12,'p_clase','aloop.py',239),
  ('clase -> TYPE ID f_startclass { cvars f_cvars funciones } f_endclass','clase',9,'p_clase','aloop.py',240),
  ('f_startclass -> <empty>','f_startclass',0,'p_f_startclass','aloop.py',243),
  ('f_clasepadre -> <empty>','f_clasepadre',0,'p_f_clasepadre','aloop.py',250),
  ('f_cvars -> <empty>','f_cvars',0,'p_f_cvars','aloop.py',256),
  ('f_endclass -> <empty>','f_endclass',0,'p_f_endclass','aloop.py',268),
  ('funciones -> funciones funcion','funciones',2,'p_funciones','aloop.py',273),
  ('funciones -> empty','funciones',1,'p_funciones','aloop.py',274),
  ('funcion -> FUNC ID f_startfunc ( params ) : tipo f_tipofunc { vars estatutos } f_endfunc','funcion',14,'p_funcion','aloop.py',277),
  ('funcion -> FUNC ID f_startfunc ( params ) : NOTHING f_nothing f_tipofunc { vars estatutos } f_endfunc','funcion',15,'p_funcion','aloop.py',278),
  ('f_startfunc -> <empty>','f_startfunc',0,'p_f_startfunc','aloop.py',281),
  ('f_nothing -> <empty>','f_nothing',0,'p_f_nothing','aloop.py',286),
  ('f_tipofunc -> <empty>','f_tipofunc',0,'p_f_tipofunc','aloop.py',291),
  ('f_endfunc -> <empty>','f_endfunc',0,'p_f_endfunc','aloop.py',295),
  ('vars -> vars DEF tipo dimension : lista_id ;','vars',7,'p_vars','aloop.py',319),
  ('vars -> vars DEF ID f_varsobj : lista_id_obj ;','vars',7,'p_vars','aloop.py',320),
  ('vars -> empty','vars',1,'p_vars','aloop.py',321),
  ('f_varsobj -> <empty>','f_varsobj',0,'p_f_varsobj','aloop.py',324),
  ('cvars -> cvars DEF tipo dimension : lista_id_in_obj ;','cvars',7,'p_cvars','aloop.py',335),
  ('cvars -> empty','cvars',1,'p_cvars','aloop.py',336),
  ('lista_id_in_obj -> ID f_vars_in_obj','lista_id_in_obj',2,'p_lista_id_in_obj','aloop.py',339),
  ('lista_id_in_obj -> lista_id_in_obj , ID f_vars_in_obj','lista_id_in_obj',4,'p_lista_id_in_obj','aloop.py',340),
  ('f_vars_in_obj -> <empty>','f_vars_in_obj',0,'p_f_vars_in_obj','aloop.py',343),
  ('lista_id -> ID f_vars','lista_id',2,'p_lista_id','aloop.py',348),
  ('lista_id -> lista_id , ID f_vars','lista_id',4,'p_lista_id','aloop.py',349),
  ('f_vars -> <empty>','f_vars',0,'p_f_vars','aloop.py',352),
  ('lista_id_obj -> ID f_vars_obj','lista_id_obj',2,'p_lista_id_obj','aloop.py',386),
  ('lista_id_obj -> lista_id_obj , ID f_vars_obj','lista_id_obj',4,'p_lista_id_obj','aloop.py',387),
  ('f_vars_obj -> <empty>','f_vars_obj',0,'p_f_vars_obj','aloop.py',390),
  ('dimension -> [ NUM f_dim1 ] f_onedim','dimension',5,'p_dimension','aloop.py',416),
  ('dimension -> [ NUM f_dim1 ] [ NUM f_dim2 ] f_twodim','dimension',9,'p_dimension','aloop.py',417),
  ('dimension -> empty','dimension',1,'p_dimension','aloop.py',418),
  ('f_dim1 -> <empty>','f_dim1',0,'p_f_dim1','aloop.py',421),
  ('f_dim2 -> <empty>','f_dim2',0,'p_f_dim2','aloop.py',436),
  ('f_onedim -> <empty>','f_onedim',0,'p_f_onedim','aloop.py',450),
  ('f_twodim -> <empty>','f_twodim',0,'p_f_twodim','aloop.py',457),
  ('tipo -> NUMBER','tipo',1,'p_tipo','aloop.py',464),
  ('tipo -> STRING','tipo',1,'p_tipo','aloop.py',465),
  ('params -> pparams','params',1,'p_params','aloop.py',473),
  ('params -> empty','params',1,'p_params','aloop.py',474),
  ('pparams -> tipo ID f_param','pparams',3,'p_pparams','aloop.py',477),
  ('pparams -> pparams , tipo ID f_param','pparams',5,'p_pparams','aloop.py',478),
  ('f_param -> <empty>','f_param',0,'p_f_param','aloop.py',481),
  ('estatutos -> estatutos estatuto','estatutos',2,'p_estatutos','aloop.py',495),
  ('estatutos -> empty','estatutos',1,'p_estatutos','aloop.py',496),
  ('estatuto -> asignacion','estatuto',1,'p_estatuto','aloop.py',499),
  ('estatuto -> while','estatuto',1,'p_estatuto','aloop.py',500),
  ('estatuto -> for','estatuto',1,'p_estatuto','aloop.py',501),
  ('estatuto -> condicion','estatuto',1,'p_estatuto','aloop.py',502),
  ('estatuto -> CALL call_func ;','estatuto',3,'p_estatuto','aloop.py',503),
  ('call_func -> func','call_func',1,'p_call_func','aloop.py',506),
  ('call_func -> input','call_func',1,'p_call_func','aloop.py',507),
  ('call_func -> write','call_func',1,'p_call_func','aloop.py',508),
  ('call_func -> to_num','call_func',1,'p_call_func','aloop.py',509),
  ('call_func -> to_str','call_func',1,'p_call_func','aloop.py',510),
  ('call_func -> return','call_func',1,'p_call_func','aloop.py',511),
  ('func -> ID f_verify_func ( args )','func',5,'p_func','aloop.py',514),
  ('func -> ID f_varobj : ID f_verify_func_composite ( args )','func',8,'p_func','aloop.py',515),
  ('f_verify_func -> <empty>','f_verify_func',0,'p_f_verify_func','aloop.py',518),
  ('f_verify_func_composite -> <empty>','f_verify_func_composite',0,'p_f_verify_func_composite','aloop.py',533),
  ('args -> args_list f_end_args','args',2,'p_args','aloop.py',553),
  ('args -> f_end_args','args',1,'p_args','aloop.py',554),
  ('args_list -> expresion f_arg','args_list',2,'p_args_list','aloop.py',557),
  ('args_list -> args_list , expresion f_arg','args_list',4,'p_args_list','aloop.py',558),
  ('f_arg -> <empty>','f_arg',0,'p_f_arg','aloop.py',561),
  ('f_end_args -> <empty>','f_end_args',0,'p_f_end_args','aloop.py',579),
  ('asignacion -> var = f_oper expresion ;','asignacion',5,'p_asignacion','aloop.py',586),
  ('var -> ID f_varobj : ID f_verify_type_composite indexacion','var',6,'p_var','aloop.py',590),
  ('var -> ID f_verify_type indexacion','var',3,'p_var','aloop.py',591),
  ('indexacion -> f_start_array [ expresion f_index ] f_end_array','indexacion',6,'p_indexacion','aloop.py',594),
  ('indexacion -> f_start_array [ expresion f_index ] [ f_next_index expresion f_index ] f_end_array','indexacion',11,'p_indexacion','aloop.py',595),
  ('indexacion -> f_no_index empty','indexacion',2,'p_indexacion','aloop.py',596),
  ('f_varobj -> <empty>','f_varobj',0,'p_f_varobj','aloop.py',599),
  ('f_verify_type -> <empty>','f_verify_type',0,'p_f_verify_type','aloop.py',604),
  ('f_verify_type_composite -> <empty>','f_verify_type_composite',0,'p_f_verify_type_composite','aloop.py',625),
  ('f_no_index -> <empty>','f_no_index',0,'p_f_no_index','aloop.py',646),
  ('f_start_array -> <empty>','f_start_array',0,'p_f_start_array','aloop.py',653),
  ('f_index -> <empty>','f_index',0,'p_f_index','aloop.py',666),
  ('f_next_index -> <empty>','f_next_index',0,'p_f_next_index','aloop.py',699),
  ('f_end_array -> <empty>','f_end_array',0,'p_f_end_array','aloop.py',705),
  ('expresion -> exp','expresion',1,'p_expresion','aloop.py',724),
  ('expresion -> expresion COMP f_oper exp f_expres','expresion',5,'p_expresion','aloop.py',725),
  ('f_expres -> <empty>','f_expres',0,'p_f_expres','aloop.py',728),
  ('exp -> term','exp',1,'p_exp','aloop.py',752),
  ('exp -> exp OPTERM f_oper term f_exp','exp',5,'p_exp','aloop.py',753),
  ('f_exp -> <empty>','f_exp',0,'p_f_exp','aloop.py',757),
  ('term -> fact','term',1,'p_term','aloop.py',781),
  ('term -> term OPFACT f_oper fact f_term','term',5,'p_term','aloop.py',782),
  ('f_term -> <empty>','f_term',0,'p_f_term','aloop.py',786),
  ('f_oper -> <empty>','f_oper',0,'p_f_oper','aloop.py',811),
  ('fact -> ( lparen expresion ) rparen','fact',5,'p_fact','aloop.py',815),
  ('fact -> var','fact',1,'p_fact','aloop.py',816),
  ('fact -> NUM f_fact','fact',2,'p_fact','aloop.py',817),
  ('fact -> OPTERM NUM','fact',2,'p_fact','aloop.py',818),
  ('fact -> CALL call_func f_return_val','fact',3,'p_fact','aloop.py',819),
  ('f_return_val -> <empty>','f_return_val',0,'p_f_return_val','aloop.py',841),
  ('lparen -> <empty>','lparen',0,'p_lparen','aloop.py',860),
  ('rparen -> <empty>','rparen',0,'p_rparen','aloop.py',864),
  ('f_fact -> <empty>','f_fact',0,'p_f_fact','aloop.py',868),
  ('condicion -> IF ( expresion ) f_if THEN { estatutos } condicionp f_endif','condicion',11,'p_condicion','aloop.py',880),
  ('condicionp -> ELSE f_else { estatutos }','condicionp',5,'p_condicionp','aloop.py',883),
  ('condicionp -> empty','condicionp',1,'p_condicionp','aloop.py',884),
  ('f_if -> <empty>','f_if',0,'p_f_if','aloop.py',887),
  ('f_endif -> <empty>','f_endif',0,'p_f_endif','aloop.py',897),
  ('f_else -> <empty>','f_else',0,'p_f_else','aloop.py',902),
  ('while -> WHILE f_while ( expresion f_exprwhile ) DO { estatutos } f_endwhile','while',11,'p_while','aloop.py',909),
  ('f_while -> <empty>','f_while',0,'p_f_while','aloop.py',912),
  ('f_exprwhile -> <empty>','f_exprwhile',0,'p_f_exprwhile','aloop.py',916),
  ('f_endwhile -> <empty>','f_endwhile',0,'p_f_endwhile','aloop.py',926),
  ('for -> FOR expresion f_for_start TO expresion f_for_to { estatutos } f_for_end','for',10,'p_for','aloop.py',933),
  ('f_for_start -> <empty>','f_for_start',0,'p_f_for_start','aloop.py',936),
  ('f_for_to -> <empty>','f_for_to',0,'p_f_for_to','aloop.py',946),
  ('f_for_end -> <empty>','f_for_end',0,'p_f_for_end','aloop.py',962),
  ('to_num -> TO_NUMBER ( STR )','to_num',4,'p_to_num','aloop.py',973),
  ('to_num -> TO_NUMBER ( var )','to_num',4,'p_to_num','aloop.py',974),
  ('to_str -> TO_STRING ( expresion )','to_str',4,'p_to_str','aloop.py',987),
  ('input -> INPUT ( var )','input',4,'p_input','aloop.py',1000),
  ('write -> PRINT ( write_list )','write',4,'p_write','aloop.py',1004),
  ('write_list -> write_list & write_listp','write_list',3,'p_write_list','aloop.py',1007),
  ('write_list -> write_listp','write_list',1,'p_write_list','aloop.py',1008),
  ('write_listp -> STR','write_listp',1,'p_write_listp','aloop.py',1011),
  ('write_listp -> var','write_listp',1,'p_write_listp','aloop.py',1012),
  ('write_listp -> CALL to_str','write_listp',2,'p_write_listp','aloop.py',1013),
  ('return -> RET ( expresion )','return',4,'p_return','aloop.py',1020),
  ('empty -> <empty>','empty',0,'p_empty','aloop.py',1040),
]
