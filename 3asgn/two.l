%{
  #define ERROR -1
  int lines = 1;
  /*
  1 - if
  2 - then
  3 - else
  4 - Identifer
  5 - Number
  6 - Relational Operator
 -1 - Invalid Input
  */
%}
ws         [ \t]
digit      [0-9]
digits     ({digit}+) 
number     ({digits}(.{digits})?(E[+-]?{digits})?)
letter     [A-Za-z]
id         {letter}({letter}|{digit})*
if         if
then       then
else       else 
relop      <|>|<=|>=|=|<>
%%
if      {return 1;}
then    {return 2;}
else    {return 3;}
{ws}     {}
{id}     {return 4;}
{number} {return 5;}
{relop}  {return 6;}
\n       {lines++;}
.        {return ERROR;}
%%

int yywrap(void){return 1;}
int main()
{
    int token ;
    yyin = fopen("myfile.txt","r");
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

    printf("No of lines - %d\n",lines );
    return 0;
}