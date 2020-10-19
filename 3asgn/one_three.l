%{
// Integer equivalent divisible by 3
%}

%%
(0|1(0(1)*0)*1)* {printf("YES");}
.*               {printf("NO");}
%%

int yywrap(void) { return 0;}
int main()
{
    yylex();
    return 0;
}