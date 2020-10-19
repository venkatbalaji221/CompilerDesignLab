%{
#define ERROR -1
int line_number=1;
%}
whitespace [ \t]
letter [a-zA-Z]
digit [0-9]
integer ({digit}+)
l_or_d ({letter}|{digit})
identifier ({letter}{l_or_d}*)
operator [-+*/]
separator [;,(){}]
%%
{integer} {return 1;}
{identifier} {return 2;}
{operator}|{separator} {return (int)yytext[0];}
{whitespace} {}
\n {line_number++;}
. {return ERROR;}
%%
int yywrap(void) {return 1;}
int main() {
int token;
yyin=fopen("myfile.txt","r");
while ((token=yylex())!=0)
printf("%d %s \n", token, yytext);
printf("lines %d \n",line_number);
}
