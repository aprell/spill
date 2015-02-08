import tokenize, parse, eval from require "spill"

------------------
-- Conditionals
------------------
-- 10 0 > if "pos" else "neg" then .

-----------
-- Loops
-----------
-- 10 begin dup . 1 - dup 0 = until clear "ZERO" .
-- 1 begin dup factorial . 1 + dup 10 > until clear

eval parse tokenize [[
: inc 1 + ;
]]

eval parse tokenize [[
: dec 1 - ;
]]

eval parse tokenize [[
: neg 0 swap - ;
]]

eval parse tokenize [[
: sq 2 ^ ;
]]

eval parse tokenize [[
: sqrt 0.5 ^ ;
]]

eval parse tokenize [[
: cube dup square * ;
]]

eval parse tokenize [[
: even? 2 % 0 = ;
]]

eval parse tokenize [[
: odd? 2 % 0 != ;
]]

eval parse tokenize [[
: mult? % 0 = ;
]]

eval parse tokenize [[
: factorial
  dup 1 > if
    dup 1 - factorial *
  then
;
]]

eval parse tokenize [[
: [a,b] 1 range ;
]]

eval parse tokenize [[
: [a,b) 1 - 1 range ;
]]

eval parse tokenize [[
: (a,b] [ 1 + ] dip 1 range ;
]]

eval parse tokenize [[
: (a,b) [ 1 + ] [ 1 - ] bi* 1 range ;
]]

eval parse tokenize [[
: spill [ ] each ;
]]

eval parse tokenize [[
: first 1 !! ;
]]

eval parse tokenize [[
: second 2 !! ;
]]

eval parse tokenize [[
: third 3 !! ;
]]

eval parse tokenize [[
: last dup length !! ;
]]

eval parse tokenize [[
: apply 1 swap times ;
]]

-- { 1 2 3 } [ 2 * ] map
eval parse tokenize [[
: map
  [ dup length ] dip swap
  [ [ each ] ] dip
  [ apply ] dip
  mkseq
;
]]

-- { 1 2 3 } [ + ] fold
eval parse tokenize [[
: fold
  [ dup length 1 - [ spill ] dip ] dip
  times
;
]]

eval parse tokenize [[
: sum [ + ] fold ;
]]

eval parse tokenize [[
: product [ * ] fold ;
]]

-- : mean dup sum swap length / ;
eval parse tokenize [[
: mean [ sum ] [ length ] bi / ;
]]

eval parse tokenize [[
: fizzbuzz
  dup 15 mult? if drop "FizzBuzz" . else
	dup 3 mult? if drop "Fizz" . else
	  dup 5 mult? if drop "Buzz" . else . then
    then
  then
;
]]

eval parse tokenize [[
: 2dip swap [ dip ] dip ;
]]
