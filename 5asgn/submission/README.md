## Assignment-5
## K.V.Balaji (17CS02001)

### Part-1
     Input: flex scan1.l
            gcc lex.yy.c
            ./a.out
            python ll.py -g grammar1.txt
### Part-2
     Input: flex scan2.l
            gcc lex.yy.c
            ./a.out
            python ll.py -g grammar2.txt

## Sample Inputs:
### part-1: (Input in input1.txt)
    1) x+y*z
    2) xy+(y*z)
    3) (x)+(z)

### part-2: (Input in input2.txt)
    1)prog
        int i;
        int j;
        i:=4;
        j:=5;
        print count
            if i>j
                then count:=4;
            else
                count:=8;
            end
      end

    2)prog
        int sum;
        int count;

        sum:=0;
        count := 5;

        scan count
        print sum

        while sum>0
            do
                count := count + 1;
                i := 1.2345;

                if count=3
                then sum:=2;
                end
            end
    end

        