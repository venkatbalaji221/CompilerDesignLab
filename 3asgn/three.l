%{
   int lines=1;
%}
ws        [ \t]
integer  (INT|int)
floatpt  (FLOAT|float)
type     ({integer}|{floatpt})
if       if 
loopvar  (for|while)
relop    <|>|<=|>=|==|<>
asgn     "="|"+="|"-="
op       "-"|"+"|"*"|"/"|"++"|"--"
sep      [;,(){}]
letter     [A-Za-z]
digit      [0-9]
id         {letter}({letter}|{digit})*
digits     ({digit}+) 
number     ({digits}(.{digits})?(E[+-]?{digits})?)
newline    ([\n])
%%

{ws}           {}
main           {return 1;}
{type}         {return 2;}
if             {return 3;}
{loopvar}      {return 4;}
read           {return 5;}
print          {return 6;}
{relop}|{asgn}|{op}  {return 7;}
{sep}          {return 8;}
{id}           {return 9;}
{number}       {return 10;}
{newline}            {lines++;}
.              {return -1;}
%%

int yywrap(void) {return 1;}
int main()
{
   int token ;
   yyin = fopen("code.txt","r");
   while( (token=yylex())!=0 )
    {
      if (token==-1)
      {
        if (*yytext != '\r')
        {
          printf("%d %s\n", token, yytext);
        }
      }
      else
      {
          printf("%d %s\n", token, yytext);

      }
    }        

   printf("No of lines - %d", lines);
   return 0;
}