
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "startCALL COMP DEF DO ELSE END FOR FUNC ID IF INPUT MAIN NOTHING NUM NUMBER OPFACT OPTERM PRINT PROGRAM RET STR STRING THEN TO TO_NUMBER TO_STRING TYPE WHILEstart : PROGRAM f_start ID f_prog ';' clases vars funciones MAIN f_main '(' ')' '{' estatutos '}' END f_end ';' f_start :f_prog :f_main :f_end : clases : clases clase\n              | emptyclase : TYPE ID f_startclass ':' ID f_clasepadre '{' cvars f_cvars funciones '}' f_endclass \n             | TYPE ID f_startclass '{' cvars f_cvars funciones '}' f_endclass f_startclass :f_clasepadre :f_cvars :f_endclass :funciones : funciones funcion\n                  | emptyfuncion : FUNC ID f_startfunc '(' params ')' ':' tipo f_tipofunc '{' vars estatutos '}' f_endfunc\n               | FUNC ID f_startfunc '(' params ')' ':' NOTHING f_nothing f_tipofunc '{' vars estatutos '}' f_endfunc f_startfunc :f_nothing :f_tipofunc :f_endfunc :vars : vars DEF tipo dimension ':' lista_id ';'\n            | vars DEF ID f_varsobj ':' lista_id ';'\n            | emptyf_varsobj :cvars : cvars DEF tipo dimension ':' lista_id ';'\n             | emptylista_id : ID f_vars\n                | lista_id ',' ID f_varsf_vars :dimension : '[' expresion f_dim1 ']' f_onedim\n                 | '[' expresion f_dim1 ']' '[' expresion f_dim2 ']' f_twodim\n                 | emptyf_dim1 :f_dim2 :f_onedim :f_twodim :tipo : NUMBER \n            | STRINGparams : pparams \n              | emptypparams : tipo ID f_param\n               | pparams ',' tipo ID f_paramf_param :estatutos : estatutos estatuto \n                 | emptyestatuto : asignacion \n                | while \n                | for \n                | condicion \n                | CALL call_func ';' call_func : func\n                 | input \n                 | write \n                 | to_num \n                 | to_str\n                 | return func : ID  f_verify_func '(' args ')'\n            | ID  f_varobj ':' ID f_verify_func_composite '(' args ')' f_verify_func :f_verify_func_composite :args : args_list\n            | emptyargs_list : expresion \n                 | args_list ',' expresionasignacion : var '=' f_oper expresion ';' var : ID f_varobj ':' ID f_verify_type_composite dimension\n           | ID f_verify_type dimensionf_varobj :f_verify_type :f_verify_type_composite :expresion : exp\n                 | expresion COMP f_oper exp f_expresf_expres :exp : term\n           | exp OPTERM f_oper term f_expf_exp :term : fact\n            | term OPFACT f_oper fact f_termf_term :f_oper :fact : '(' lparen expresion ')' rparen\n            | var\n            | NUM f_fact\n            | OPTERM NUM\n            | CALL call_funclparen :rparen :f_fact :condicion : IF '(' expresion ')' f_if THEN '{' estatutos '}' condicionp f_endifcondicionp : ELSE f_else '{' estatutos '}'\n                  | empty f_if :f_endif :f_else :while : WHILE f_while '(' expresion f_exprwhile ')' DO '{' estatutos '}' f_endwhile f_while :f_exprwhile :f_endwhile :for : FOR expresion f_for_start TO expresion f_for_to '{' estatutos '}' f_for_end f_for_start :f_for_to :f_for_end :to_num : TO_NUMBER '(' STR ')' \n              | TO_NUMBER '(' var ')' to_str : TO_STRING '(' expresion ')' input : INPUT '(' var ')' write : PRINT '(' write_list ')' write_list : write_list '&' write_listp\n                  | write_listpwrite_listp : STR \n                   | var \n                   | CALL to_strreturn : RET '(' expresion ')' empty :"
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,202,],[0,-1,]),'ID':([2,3,11,12,14,19,22,23,28,31,35,41,44,46,55,56,57,59,80,82,85,86,89,90,91,95,96,97,98,99,100,102,106,107,112,118,119,135,136,137,138,139,140,143,147,161,170,173,176,182,189,190,191,199,205,207,212,216,217,222,223,225,226,228,229,230,231,234,235,236,238,239,240,242,243,244,246,247,248,],[-2,4,-24,16,21,26,-38,-39,45,47,53,-87,68,53,-81,-81,-81,45,-115,109,-22,111,45,45,45,45,45,45,45,45,130,-23,45,-46,45,45,158,-45,-47,-48,-49,-50,68,45,179,45,53,-81,45,45,-51,45,45,45,45,-115,-66,-115,-115,45,-115,-115,-115,45,-115,45,45,45,-103,-115,-99,-100,-94,-92,-96,-90,-115,45,-91,]),';':([4,5,29,37,38,40,42,43,45,52,53,58,60,61,62,63,64,65,66,67,75,76,87,88,101,111,113,114,115,116,117,130,148,150,151,152,153,159,160,163,164,165,166,167,171,172,181,185,187,188,197,203,209,218,],[-3,6,-33,-72,-75,-78,-83,-89,-70,85,-30,-85,-84,-86,-52,-53,-54,-55,-56,-57,-115,102,-28,-36,-68,-30,-31,-74,-77,-80,-88,-71,-29,-73,-76,-79,-82,-107,-108,-104,-105,-106,-114,-115,-5,189,-58,-67,201,202,-37,212,-32,-59,]),'TYPE':([6,7,8,10,132,169,200,211,],[-115,12,-7,-6,-13,-9,-13,-8,]),'DEF':([6,7,8,9,10,11,32,48,49,85,102,103,131,132,169,200,201,207,211,216,217,223,],[-115,-115,-7,14,-6,-24,-115,79,-27,-22,-23,-115,79,-13,-9,-13,-26,-115,-8,14,-115,14,]),'MAIN':([6,7,8,9,10,11,13,15,18,85,102,132,169,200,211,227,232,233,237,],[-115,-115,-7,-115,-6,-24,17,-15,-14,-22,-23,-13,-9,-13,-8,-21,-16,-21,-17,]),'FUNC':([6,7,8,9,10,11,13,15,18,32,48,49,78,85,102,103,104,131,132,168,169,186,200,201,211,227,232,233,237,],[-115,-115,-7,-115,-6,-24,19,-15,-14,-115,-12,-27,-115,-22,-23,-115,19,-12,-13,-115,-9,19,-13,-26,-8,-21,-16,-21,-17,]),'}':([11,15,18,32,48,49,78,80,85,102,103,104,106,107,131,135,136,137,138,139,168,186,189,201,207,212,216,217,222,223,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,242,243,244,246,247,248,],[-24,-15,-14,-115,-12,-27,-115,-115,-22,-23,-115,132,134,-46,-12,-45,-47,-48,-49,-50,-115,200,-51,-26,-115,-66,-115,-115,227,-115,-115,-115,-21,233,-115,235,236,-16,-21,238,-103,-115,-17,-99,-100,-94,-92,-96,-90,-115,248,-91,]),'CALL':([11,28,41,55,56,57,59,80,85,89,90,91,96,98,99,102,106,107,112,118,135,136,137,138,139,143,161,173,176,182,189,190,191,199,205,207,212,216,217,222,223,225,226,228,229,230,231,234,235,236,238,239,240,242,243,244,246,247,248,],[-24,44,-87,-81,-81,-81,44,-115,-22,44,44,44,125,44,44,-23,140,-46,44,44,-45,-47,-48,-49,-50,44,125,-81,44,44,-51,44,44,44,44,-115,-66,-115,-115,140,-115,-115,-115,140,-115,140,140,140,-103,-115,-99,-100,-94,-92,-96,-90,-115,140,-91,]),'WHILE':([11,80,85,102,106,107,135,136,137,138,139,189,207,212,216,217,222,223,225,226,228,229,230,231,234,235,236,238,239,240,242,243,244,246,247,248,],[-24,-115,-22,-23,142,-46,-45,-47,-48,-49,-50,-51,-115,-66,-115,-115,142,-115,-115,-115,142,-115,142,142,142,-103,-115,-99,-100,-94,-92,-96,-90,-115,142,-91,]),'FOR':([11,80,85,102,106,107,135,136,137,138,139,189,207,212,216,217,222,223,225,226,228,229,230,231,234,235,236,238,239,240,242,243,244,246,247,248,],[-24,-115,-22,-23,143,-46,-45,-47,-48,-49,-50,-51,-115,-66,-115,-115,143,-115,-115,-115,143,-115,143,143,143,-103,-115,-99,-100,-94,-92,-96,-90,-115,143,-91,]),'IF':([11,80,85,102,106,107,135,136,137,138,139,189,207,212,216,217,222,223,225,226,228,229,230,231,234,235,236,238,239,240,242,243,244,246,247,248,],[-24,-115,-22,-23,144,-46,-45,-47,-48,-49,-50,-51,-115,-66,-115,-115,144,-115,-115,-115,144,-115,144,144,144,-103,-115,-99,-100,-94,-92,-96,-90,-115,144,-91,]),'NUMBER':([14,51,79,110,145,],[22,22,22,22,22,]),'STRING':([14,51,79,110,145,],[23,23,23,23,23,]),':':([16,20,21,22,23,24,27,29,30,45,68,74,88,94,105,108,113,133,197,209,],[-10,-115,-25,-38,-39,31,35,-33,46,-69,-69,100,-36,119,-115,145,-31,170,-37,-32,]),'{':([16,22,23,24,29,37,38,40,42,43,45,47,50,58,60,61,62,63,64,65,66,67,75,77,88,101,113,114,115,116,117,130,150,151,152,153,159,160,163,164,165,166,167,177,178,181,185,194,195,197,208,209,214,218,220,221,224,241,245,],[-10,-38,-39,32,-33,-72,-75,-78,-83,-89,-70,-11,80,-85,-84,-86,-52,-53,-54,-55,-56,-57,-115,103,-36,-68,-31,-74,-77,-80,-88,-71,-73,-76,-79,-82,-107,-108,-104,-105,-106,-114,-115,-20,-19,-58,-67,207,-20,-37,217,-32,-102,-59,225,226,229,-95,246,]),'(':([17,25,26,28,34,41,55,56,57,59,68,69,70,71,72,73,89,90,91,93,98,99,112,118,142,143,144,158,173,174,176,182,183,190,191,199,205,],[-4,33,-18,41,51,-87,-81,-81,-81,41,-60,95,96,97,98,99,41,41,41,118,41,41,41,41,-97,41,176,-61,-81,191,41,41,199,41,41,41,41,]),'[':([20,22,23,45,75,88,105,130,167,],[28,-38,-39,-70,28,112,28,-71,28,]),'NUM':([28,39,41,55,56,57,59,89,90,91,98,99,112,118,143,173,176,182,190,191,199,205,],[43,58,-87,-81,-81,-81,43,43,43,43,43,43,43,43,43,-81,43,43,43,43,43,43,]),'OPTERM':([28,29,37,38,40,41,42,43,45,55,56,57,58,59,60,61,62,63,64,65,66,67,75,88,89,90,91,98,99,101,112,113,114,115,116,117,118,130,143,151,152,153,159,160,163,164,165,166,167,173,176,181,182,185,190,191,197,199,205,209,218,],[39,-33,56,-75,-78,-87,-83,-89,-70,-81,-81,-81,-85,39,-84,-86,-52,-53,-54,-55,-56,-57,-115,-36,39,39,39,39,39,-68,39,-31,56,-77,-80,-88,39,-71,39,-76,-79,-82,-107,-108,-104,-105,-106,-114,-115,-81,39,-58,39,-67,39,39,-37,39,39,-32,-59,]),'OPFACT':([29,38,40,42,43,45,58,60,61,62,63,64,65,66,67,75,88,101,113,115,116,117,130,152,153,159,160,163,164,165,166,167,181,185,197,209,218,],[-33,57,-78,-83,-89,-70,-85,-84,-86,-52,-53,-54,-55,-56,-57,-115,-36,-68,-31,57,-80,-88,-71,-79,-82,-107,-108,-104,-105,-106,-114,-115,-58,-67,-37,-32,-59,]),'COMP':([29,36,37,38,40,42,43,45,58,60,61,62,63,64,65,66,67,75,88,92,101,113,114,115,116,117,128,129,130,149,150,151,152,153,157,159,160,163,164,165,166,167,175,181,185,193,197,198,203,204,209,214,218,],[-33,55,-72,-75,-78,-83,-89,-70,-85,-84,-86,-52,-53,-54,-55,-56,-57,-115,-36,55,-68,-31,-74,-77,-80,-88,55,55,-71,55,-73,-76,-79,-82,55,-107,-108,-104,-105,-106,-114,-115,55,-58,-67,55,-37,55,55,55,-32,55,-59,]),']':([29,36,37,38,40,42,43,45,54,58,60,61,62,63,64,65,66,67,75,88,101,113,114,115,116,117,130,149,150,151,152,153,159,160,163,164,165,166,167,180,181,185,197,209,218,],[-33,-34,-72,-75,-78,-83,-89,-70,88,-85,-84,-86,-52,-53,-54,-55,-56,-57,-115,-36,-68,-31,-74,-77,-80,-88,-71,-35,-73,-76,-79,-82,-107,-108,-104,-105,-106,-114,-115,197,-58,-67,-37,-32,-59,]),')':([29,33,37,38,40,42,43,45,51,58,60,61,62,63,64,65,66,67,75,81,83,84,88,92,101,109,113,114,115,116,117,118,120,121,122,123,124,126,127,128,129,130,146,150,151,152,153,154,155,156,157,159,160,162,163,164,165,166,167,179,181,184,185,193,196,197,198,199,204,209,210,213,218,],[-33,50,-72,-75,-78,-83,-89,-70,-115,-85,-84,-86,-52,-53,-54,-55,-56,-57,-115,108,-40,-41,-36,117,-68,-44,-31,-74,-77,-80,-88,-115,159,160,-110,-111,-112,163,164,165,166,-71,-42,-73,-76,-79,-82,181,-62,-63,-64,-107,-108,-113,-104,-105,-106,-114,-115,-44,-58,-109,-67,206,-43,-37,-65,-115,-98,-32,218,219,-59,]),',':([29,37,38,40,42,43,45,52,53,58,60,61,62,63,64,65,66,67,75,76,83,87,88,101,109,111,113,114,115,116,117,130,146,148,150,151,152,153,155,157,159,160,163,164,165,166,167,179,181,185,187,196,197,198,209,218,],[-33,-72,-75,-78,-83,-89,-70,86,-30,-85,-84,-86,-52,-53,-54,-55,-56,-57,-115,86,110,-28,-36,-68,-44,-30,-31,-74,-77,-80,-88,-71,-42,-29,-73,-76,-79,-82,182,-64,-107,-108,-104,-105,-106,-114,-115,-44,-58,-67,86,-43,-37,-65,-32,-59,]),'TO':([29,37,38,40,42,43,45,58,60,61,62,63,64,65,66,67,75,88,101,113,114,115,116,117,130,150,151,152,153,159,160,163,164,165,166,167,175,181,185,192,197,209,218,],[-33,-72,-75,-78,-83,-89,-70,-85,-84,-86,-52,-53,-54,-55,-56,-57,-115,-36,-68,-31,-74,-77,-80,-88,-71,-73,-76,-79,-82,-107,-108,-104,-105,-106,-114,-115,-101,-58,-67,205,-37,-32,-59,]),'&':([29,45,75,88,101,113,121,122,123,124,130,162,165,167,184,185,197,209,],[-33,-70,-115,-36,-68,-31,161,-110,-111,-112,-71,-113,-106,-115,-109,-67,-37,-32,]),'=':([29,45,75,88,101,113,130,141,167,185,197,209,],[-33,-70,-115,-36,-68,-31,-71,173,-115,-67,-37,-32,]),'INPUT':([44,140,],[69,69,]),'PRINT':([44,140,],[70,70,]),'TO_NUMBER':([44,140,],[71,71,]),'TO_STRING':([44,125,140,],[72,72,72,]),'RET':([44,140,],[73,73,]),'STR':([96,97,161,],[123,126,123,]),'END':([134,],[171,]),'NOTHING':([145,],[178,]),'THEN':([206,215,],[-93,221,]),'DO':([219,],[224,]),'ELSE':([236,],[241,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'f_start':([2,],[3,]),'f_prog':([4,],[5,]),'clases':([6,],[7,]),'empty':([6,7,9,20,32,51,75,78,80,103,105,118,167,168,199,207,216,217,223,225,226,229,236,246,],[8,11,15,29,49,84,29,15,107,49,29,156,29,15,156,11,107,11,107,107,107,107,242,107,]),'vars':([7,207,217,],[9,216,223,]),'clase':([7,],[10,]),'funciones':([9,78,168,],[13,104,186,]),'funcion':([13,104,186,],[18,18,18,]),'tipo':([14,51,79,110,145,],[20,82,105,147,177,]),'f_startclass':([16,],[24,]),'f_main':([17,],[25,]),'dimension':([20,75,105,167,],[27,101,133,185,]),'f_varsobj':([21,],[30,]),'f_startfunc':([26,],[34,]),'expresion':([28,59,98,99,112,118,143,176,182,190,191,199,205,],[36,92,128,129,149,157,175,193,198,203,204,157,214,]),'exp':([28,59,89,98,99,112,118,143,176,182,190,191,199,205,],[37,37,114,37,37,37,37,37,37,37,37,37,37,37,]),'term':([28,59,89,90,98,99,112,118,143,176,182,190,191,199,205,],[38,38,38,115,38,38,38,38,38,38,38,38,38,38,38,]),'fact':([28,59,89,90,91,98,99,112,118,143,176,182,190,191,199,205,],[40,40,40,40,116,40,40,40,40,40,40,40,40,40,40,40,]),'var':([28,59,89,90,91,95,96,97,98,99,106,112,118,143,161,176,182,190,191,199,205,222,228,230,231,234,247,],[42,42,42,42,42,120,124,127,42,42,141,42,42,42,124,42,42,42,42,42,42,141,141,141,141,141,141,]),'cvars':([32,103,],[48,131,]),'lista_id':([35,46,170,],[52,76,187,]),'f_dim1':([36,],[54,]),'lparen':([41,],[59,]),'f_fact':([43,],[60,]),'call_func':([44,140,],[61,172,]),'func':([44,140,],[62,62,]),'input':([44,140,],[63,63,]),'write':([44,140,],[64,64,]),'to_num':([44,140,],[65,65,]),'to_str':([44,125,140,],[66,162,66,]),'return':([44,140,],[67,67,]),'f_varobj':([45,68,],[74,94,]),'f_verify_type':([45,],[75,]),'f_clasepadre':([47,],[77,]),'f_cvars':([48,131,],[78,168,]),'params':([51,],[81,]),'pparams':([51,],[83,]),'f_vars':([53,111,],[87,148,]),'f_oper':([55,56,57,173,],[89,90,91,190,]),'f_verify_func':([68,],[93,]),'estatutos':([80,216,223,225,226,229,246,],[106,222,228,230,231,234,247,]),'f_onedim':([88,],[113,]),'write_list':([96,],[121,]),'write_listp':([96,161,],[122,184,]),'estatuto':([106,222,228,230,231,234,247,],[135,135,135,135,135,135,135,]),'asignacion':([106,222,228,230,231,234,247,],[136,136,136,136,136,136,136,]),'while':([106,222,228,230,231,234,247,],[137,137,137,137,137,137,137,]),'for':([106,222,228,230,231,234,247,],[138,138,138,138,138,138,138,]),'condicion':([106,222,228,230,231,234,247,],[139,139,139,139,139,139,139,]),'f_param':([109,179,],[146,196,]),'f_expres':([114,],[150,]),'f_exp':([115,],[151,]),'f_term':([116,],[152,]),'rparen':([117,],[153,]),'args':([118,199,],[154,210,]),'args_list':([118,199,],[155,155,]),'f_verify_type_composite':([130,],[167,]),'f_endclass':([132,200,],[169,211,]),'f_while':([142,],[174,]),'f_dim2':([149,],[180,]),'f_verify_func_composite':([158,],[183,]),'f_end':([171,],[188,]),'f_for_start':([175,],[192,]),'f_tipofunc':([177,195,],[194,208,]),'f_nothing':([178,],[195,]),'f_twodim':([197,],[209,]),'f_exprwhile':([204,],[213,]),'f_if':([206,],[215,]),'f_for_to':([214,],[220,]),'f_endfunc':([227,233,],[232,237,]),'f_for_end':([235,],[239,]),'condicionp':([236,],[240,]),'f_endwhile':([238,],[243,]),'f_endif':([240,],[244,]),'f_else':([241,],[245,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> PROGRAM f_start ID f_prog ; clases vars funciones MAIN f_main ( ) { estatutos } END f_end ;','start',18,'p_start','aloop.py',114),
  ('f_start -> <empty>','f_start',0,'p_f_start','aloop.py',117),
  ('f_prog -> <empty>','f_prog',0,'p_f_prog','aloop.py',125),
  ('f_main -> <empty>','f_main',0,'p_f_main','aloop.py',130),
  ('f_end -> <empty>','f_end',0,'p_f_end','aloop.py',134),
  ('clases -> clases clase','clases',2,'p_clases','aloop.py',142),
  ('clases -> empty','clases',1,'p_clases','aloop.py',143),
  ('clase -> TYPE ID f_startclass : ID f_clasepadre { cvars f_cvars funciones } f_endclass','clase',12,'p_clase','aloop.py',146),
  ('clase -> TYPE ID f_startclass { cvars f_cvars funciones } f_endclass','clase',9,'p_clase','aloop.py',147),
  ('f_startclass -> <empty>','f_startclass',0,'p_f_startclass','aloop.py',150),
  ('f_clasepadre -> <empty>','f_clasepadre',0,'p_f_clasepadre','aloop.py',157),
  ('f_cvars -> <empty>','f_cvars',0,'p_f_cvars','aloop.py',163),
  ('f_endclass -> <empty>','f_endclass',0,'p_f_endclass','aloop.py',167),
  ('funciones -> funciones funcion','funciones',2,'p_funciones','aloop.py',172),
  ('funciones -> empty','funciones',1,'p_funciones','aloop.py',173),
  ('funcion -> FUNC ID f_startfunc ( params ) : tipo f_tipofunc { vars estatutos } f_endfunc','funcion',14,'p_funcion','aloop.py',176),
  ('funcion -> FUNC ID f_startfunc ( params ) : NOTHING f_nothing f_tipofunc { vars estatutos } f_endfunc','funcion',15,'p_funcion','aloop.py',177),
  ('f_startfunc -> <empty>','f_startfunc',0,'p_f_startfunc','aloop.py',180),
  ('f_nothing -> <empty>','f_nothing',0,'p_f_nothing','aloop.py',185),
  ('f_tipofunc -> <empty>','f_tipofunc',0,'p_f_tipofunc','aloop.py',190),
  ('f_endfunc -> <empty>','f_endfunc',0,'p_f_endfunc','aloop.py',194),
  ('vars -> vars DEF tipo dimension : lista_id ;','vars',7,'p_vars','aloop.py',200),
  ('vars -> vars DEF ID f_varsobj : lista_id ;','vars',7,'p_vars','aloop.py',201),
  ('vars -> empty','vars',1,'p_vars','aloop.py',202),
  ('f_varsobj -> <empty>','f_varsobj',0,'p_f_varsobj','aloop.py',205),
  ('cvars -> cvars DEF tipo dimension : lista_id ;','cvars',7,'p_cvars','aloop.py',216),
  ('cvars -> empty','cvars',1,'p_cvars','aloop.py',217),
  ('lista_id -> ID f_vars','lista_id',2,'p_lista_id','aloop.py',220),
  ('lista_id -> lista_id , ID f_vars','lista_id',4,'p_lista_id','aloop.py',221),
  ('f_vars -> <empty>','f_vars',0,'p_f_vars','aloop.py',224),
  ('dimension -> [ expresion f_dim1 ] f_onedim','dimension',5,'p_dimension','aloop.py',244),
  ('dimension -> [ expresion f_dim1 ] [ expresion f_dim2 ] f_twodim','dimension',9,'p_dimension','aloop.py',245),
  ('dimension -> empty','dimension',1,'p_dimension','aloop.py',246),
  ('f_dim1 -> <empty>','f_dim1',0,'p_f_dim1','aloop.py',249),
  ('f_dim2 -> <empty>','f_dim2',0,'p_f_dim2','aloop.py',254),
  ('f_onedim -> <empty>','f_onedim',0,'p_f_onedim','aloop.py',259),
  ('f_twodim -> <empty>','f_twodim',0,'p_f_twodim','aloop.py',266),
  ('tipo -> NUMBER','tipo',1,'p_tipo','aloop.py',273),
  ('tipo -> STRING','tipo',1,'p_tipo','aloop.py',274),
  ('params -> pparams','params',1,'p_params','aloop.py',282),
  ('params -> empty','params',1,'p_params','aloop.py',283),
  ('pparams -> tipo ID f_param','pparams',3,'p_pparams','aloop.py',286),
  ('pparams -> pparams , tipo ID f_param','pparams',5,'p_pparams','aloop.py',287),
  ('f_param -> <empty>','f_param',0,'p_f_param','aloop.py',290),
  ('estatutos -> estatutos estatuto','estatutos',2,'p_estatutos','aloop.py',295),
  ('estatutos -> empty','estatutos',1,'p_estatutos','aloop.py',296),
  ('estatuto -> asignacion','estatuto',1,'p_estatuto','aloop.py',299),
  ('estatuto -> while','estatuto',1,'p_estatuto','aloop.py',300),
  ('estatuto -> for','estatuto',1,'p_estatuto','aloop.py',301),
  ('estatuto -> condicion','estatuto',1,'p_estatuto','aloop.py',302),
  ('estatuto -> CALL call_func ;','estatuto',3,'p_estatuto','aloop.py',303),
  ('call_func -> func','call_func',1,'p_call_func','aloop.py',306),
  ('call_func -> input','call_func',1,'p_call_func','aloop.py',307),
  ('call_func -> write','call_func',1,'p_call_func','aloop.py',308),
  ('call_func -> to_num','call_func',1,'p_call_func','aloop.py',309),
  ('call_func -> to_str','call_func',1,'p_call_func','aloop.py',310),
  ('call_func -> return','call_func',1,'p_call_func','aloop.py',311),
  ('func -> ID f_verify_func ( args )','func',5,'p_func','aloop.py',314),
  ('func -> ID f_varobj : ID f_verify_func_composite ( args )','func',8,'p_func','aloop.py',315),
  ('f_verify_func -> <empty>','f_verify_func',0,'p_f_verify_func','aloop.py',318),
  ('f_verify_func_composite -> <empty>','f_verify_func_composite',0,'p_f_verify_func_composite','aloop.py',328),
  ('args -> args_list','args',1,'p_args','aloop.py',341),
  ('args -> empty','args',1,'p_args','aloop.py',342),
  ('args_list -> expresion','args_list',1,'p_args_list','aloop.py',345),
  ('args_list -> args_list , expresion','args_list',3,'p_args_list','aloop.py',346),
  ('asignacion -> var = f_oper expresion ;','asignacion',5,'p_asignacion','aloop.py',349),
  ('var -> ID f_varobj : ID f_verify_type_composite dimension','var',6,'p_var','aloop.py',353),
  ('var -> ID f_verify_type dimension','var',3,'p_var','aloop.py',354),
  ('f_varobj -> <empty>','f_varobj',0,'p_f_varobj','aloop.py',357),
  ('f_verify_type -> <empty>','f_verify_type',0,'p_f_verify_type','aloop.py',362),
  ('f_verify_type_composite -> <empty>','f_verify_type_composite',0,'p_f_verify_type_composite','aloop.py',374),
  ('expresion -> exp','expresion',1,'p_expresion','aloop.py',388),
  ('expresion -> expresion COMP f_oper exp f_expres','expresion',5,'p_expresion','aloop.py',389),
  ('f_expres -> <empty>','f_expres',0,'p_f_expres','aloop.py',392),
  ('exp -> term','exp',1,'p_exp','aloop.py',416),
  ('exp -> exp OPTERM f_oper term f_exp','exp',5,'p_exp','aloop.py',417),
  ('f_exp -> <empty>','f_exp',0,'p_f_exp','aloop.py',421),
  ('term -> fact','term',1,'p_term','aloop.py',445),
  ('term -> term OPFACT f_oper fact f_term','term',5,'p_term','aloop.py',446),
  ('f_term -> <empty>','f_term',0,'p_f_term','aloop.py',450),
  ('f_oper -> <empty>','f_oper',0,'p_f_oper','aloop.py',475),
  ('fact -> ( lparen expresion ) rparen','fact',5,'p_fact','aloop.py',479),
  ('fact -> var','fact',1,'p_fact','aloop.py',480),
  ('fact -> NUM f_fact','fact',2,'p_fact','aloop.py',481),
  ('fact -> OPTERM NUM','fact',2,'p_fact','aloop.py',482),
  ('fact -> CALL call_func','fact',2,'p_fact','aloop.py',483),
  ('lparen -> <empty>','lparen',0,'p_lparen','aloop.py',505),
  ('rparen -> <empty>','rparen',0,'p_rparen','aloop.py',509),
  ('f_fact -> <empty>','f_fact',0,'p_f_fact','aloop.py',513),
  ('condicion -> IF ( expresion ) f_if THEN { estatutos } condicionp f_endif','condicion',11,'p_condicion','aloop.py',526),
  ('condicionp -> ELSE f_else { estatutos }','condicionp',5,'p_condicionp','aloop.py',529),
  ('condicionp -> empty','condicionp',1,'p_condicionp','aloop.py',530),
  ('f_if -> <empty>','f_if',0,'p_f_if','aloop.py',533),
  ('f_endif -> <empty>','f_endif',0,'p_f_endif','aloop.py',543),
  ('f_else -> <empty>','f_else',0,'p_f_else','aloop.py',548),
  ('while -> WHILE f_while ( expresion f_exprwhile ) DO { estatutos } f_endwhile','while',11,'p_while','aloop.py',555),
  ('f_while -> <empty>','f_while',0,'p_f_while','aloop.py',558),
  ('f_exprwhile -> <empty>','f_exprwhile',0,'p_f_exprwhile','aloop.py',562),
  ('f_endwhile -> <empty>','f_endwhile',0,'p_f_endwhile','aloop.py',572),
  ('for -> FOR expresion f_for_start TO expresion f_for_to { estatutos } f_for_end','for',10,'p_for','aloop.py',579),
  ('f_for_start -> <empty>','f_for_start',0,'p_f_for_start','aloop.py',582),
  ('f_for_to -> <empty>','f_for_to',0,'p_f_for_to','aloop.py',592),
  ('f_for_end -> <empty>','f_for_end',0,'p_f_for_end','aloop.py',608),
  ('to_num -> TO_NUMBER ( STR )','to_num',4,'p_to_num','aloop.py',620),
  ('to_num -> TO_NUMBER ( var )','to_num',4,'p_to_num','aloop.py',621),
  ('to_str -> TO_STRING ( expresion )','to_str',4,'p_to_str','aloop.py',634),
  ('input -> INPUT ( var )','input',4,'p_input','aloop.py',647),
  ('write -> PRINT ( write_list )','write',4,'p_write','aloop.py',651),
  ('write_list -> write_list & write_listp','write_list',3,'p_write_list','aloop.py',654),
  ('write_list -> write_listp','write_list',1,'p_write_list','aloop.py',655),
  ('write_listp -> STR','write_listp',1,'p_write_listp','aloop.py',658),
  ('write_listp -> var','write_listp',1,'p_write_listp','aloop.py',659),
  ('write_listp -> CALL to_str','write_listp',2,'p_write_listp','aloop.py',660),
  ('return -> RET ( expresion )','return',4,'p_return','aloop.py',667),
  ('empty -> <empty>','empty',0,'p_empty','aloop.py',671),
]
