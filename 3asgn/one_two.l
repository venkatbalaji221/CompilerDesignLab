%{
// even no of 0s and 1s
%}

%%
(11|00|(10|01)(11|00)*(10|01))* {printf("YES");}
.*                {printf("NO");}
%%

int yywrap(void) {return 1;}
int main()
{
    yylex();
    return 0;
}