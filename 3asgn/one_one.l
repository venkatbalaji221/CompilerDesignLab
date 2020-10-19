%{
// even no of 0s
// (1)*(0(1)*0(1)*)* {printf("YES");}
%}

%%
a*b            {printf("T1");}
(a|b)*b        {printf("T2");}
c*             {printf("T3");}    
.*             {printf("NO");}
%%

int yywrap(void) {return 1;}
int main()
{
    yylex();
    return 0;
}