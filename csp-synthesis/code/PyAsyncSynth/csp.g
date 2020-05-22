grammar csp;

cspStream
    : extMessages initialState procAlgebra;

extMessages
	: extMessage+;

extMessage
	: CHANNEL chan_name=(MID | PID) COLON trans_vals=domainSet SEMI;

domainSet
	: LCURLY MID (COMMA MID)* RCURLY;

initialState
    : INITIAL state_name=PID SEMI;

procAlgebra
    : procStmt+;

procStmt
    : state_name=PID ASSIGN transitionAlternatives SEMI;

transitionAlternatives
    : transition (BAR transition)*;

transition
    : trans_val=MID ARROW state_name=PID;



////////////////
// lexer
CHANNEL		: 'chan';
INITIAL     : 'initial'; 

SEMI		: ';';
COLON		: ':';
LCURLY		: '{';
RCURLY		: '}';
COMMA		: ',';
ASSIGN		: ':=';
BAR			: '|';
ARROW		: '->';

MID			: ('a'..'z') ('a'..'z'|'A'..'Z'|'0'..'9'|'_'|'.')*;
PID			: ('A'..'Z') ('a'..'z'|'A'..'Z'|'0'..'9'|'_'|'.')*;
//ID			: ('a'..'z'|'A'..'Z') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*;
INT			: DIGIT+;
DIGIT		: ('0'..'9');

comment		: LINECOMMENT;	//TODO: include multiline comment and return the text of comment
LINECOMMENT	: ('#') ~('\r'|'\n')* -> channel (HIDDEN);
WS			: [ \r\n\t]+ -> channel (HIDDEN);




