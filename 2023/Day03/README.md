# Day 03
[Day 03](https://adventofcode.com/2023/day/3)

## Optimazation
So I thought that we can futher optimize by tracking position of symbols only for current line and previous two.  
Then we could move this 3 line window of symbols and the second line would also check the numbers (as all numbers are horizontal).

But looking at the input, and how a few symbols are there I decided to just keep them in set/dict and go two times.  


