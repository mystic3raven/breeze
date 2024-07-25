grammar breeze;

// Parser rules
program         : statement* EOF ;

statement       : variableDeclaration
                | functionDeclaration
                | actorDeclaration
                | serviceDeclaration
                | gpuFunctionDeclaration
                | expressionStatement
                | importStatement
                ;

importStatement : 'import' modulePath ';' ;

modulePath      : ID ('.' ID)* ;

variableDeclaration
                : 'let' ID (':' type)? '=' expression ';'
                | 'var' ID (':' type)? '=' expression ';'
                ;

functionDeclaration
                : 'fn' ID '<' templateParameters '>'? '(' parameterList? ')' '->' type '{' statement* '}' ;

gpuFunctionDeclaration
                : 'gpu' 'fn' ID '(' parameterList? ')' '->' type '{' statement* '}' ;

templateParameters
                : ID (',' ID)* ;

parameterList   : parameter (',' parameter)* ;

parameter       : ID ':' type ;

actorDeclaration
                : 'actor' ID '{' actorBody '}' ;

actorBody       : actorVariableDeclaration* actorFunctionDeclaration* actorMessageHandler* ;

actorVariableDeclaration
                : 'var' ID ':' type '=' expression ';' ;

actorFunctionDeclaration
                : 'fn' ID '(' parameterList? ')' '->' type '{' statement* '}' ;

actorMessageHandler
                : 'receive' '{' caseBranch+ '}' ;

caseBranch      : 'case' ID '(' parameterList? ')' ':' statement* ;

serviceDeclaration
                : 'service' ID '{' endpointDeclaration* '}' ;

endpointDeclaration
                : 'endpoint' ID '(' parameterList? ')' '->' type '{' statement* '}' ;

expressionStatement
                : expression ';' ;

expression      : primary
                | expression binaryOperator expression
                | ID LPAREN argumentList RPAREN
                ;

primary         : ID
                | NUMBER
                | STRING
                | BOOL
                | LPAREN expression RPAREN
                ;

argumentList    : expression (',' expression)* ;

binaryOperator  : '+' | '-' | '*' | '/' | '==' | '!=' | '<' | '>' | '<=' | '>=' ;

type            : 'Int'
                | 'Float'
                | 'String'
                | 'Bool'
                | 'Void'
                | 'Channel' '<' type '>'
                | ID ('<' type (',' type)* '>')?
                ;

// Lexer rules
ID              : [a-zA-Z_][a-zA-Z_0-9]* ;
NUMBER          : [0-9]+ ;
STRING          : '"' (~["\\r\n] | '\' .)* '"' ;
BOOL            : 'true' | 'false' ;

WS              : [ \t\r\n]+ -> skip ;
COMMENT         : '//' ~[\r\n]* -> skip ;
MULTILINE_COMMENT
                : '/*' .*? '*/' -> skip ;
