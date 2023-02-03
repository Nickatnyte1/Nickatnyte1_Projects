(*
Nick Pietras
Programming Languages
Project 1
Created September 14, 2022
Last updated October 6, 2022
*)

fun asList ("a",0) = [[#"x",#"o"],[#"o",#"o"]]
  | asList ("a",1) = [[#"o",#"x"],[#"o",#"o"]]
  | asList ("a",2) = [[#"o",#"o"],[#"o",#"x"]]
  | asList ("a",3) = [[#"o",#"o"],[#"x",#"o"]]
  | asList ("b",0) = [[#"#",#"+"],[#"+",#"+"]]
  | asList ("b",1) = [[#"+",#"#"],[#"+",#"+"]]
  | asList ("b",2) = [[#"+",#"+"],[#"+",#"#"]]
  | asList ("b",3) = [[#"+",#"+"],[#"#",#"+"]];


fun stringHead atom = implode (hd (asList atom));

fun stringTail atom = implode (hd (tl (asList atom)));

fun headRowQuilt [] = "" | headRowQuilt quiltRow = stringHead (hd quiltRow)  ^ headRowQuilt(tl quiltRow);

fun tailRowQuilt [] = "" | tailRowQuilt quiltRow = stringTail (hd quiltRow)  ^ tailRowQuilt(tl quiltRow);

fun twoRows quiltRow = "\n" ^ headRowQuilt quiltRow ^ "\n" ^ tailRowQuilt quiltRow;

fun quiltToString [] = "" | quiltToString quilt = twoRows (hd quilt) ^ quiltToString (tl quilt);

fun stringConcat [] = "" | stringConcat listOfCharacters = hd listOfCharacters ^ stringConcat (tl listOfCharacters);


fun rotate (x,3) = (x,0)
  | rotate (x,n) = (x,n+1);


fun sew ([],[]) = [] | sew(quilt1, quilt2) = if tl quilt1 = [] orelse tl quilt2 = [] then [hd quilt1 @ hd quilt2]
else (hd quilt1 @ hd quilt2) :: sew(tl quilt1, tl quilt2);

fun turn quilt = 
let
  fun rowsToColumns quilt = 
  let
    fun getHeadColumn [] = [] | getHeadColumn quilt = hd (hd quilt) ::                 getHeadColumn (tl quilt)
    fun getTailColumn [] = [] | getTailColumn quilt = tl (hd quilt) ::
      getTailColumn (tl quilt)
  in
    if hd quilt = [] then [] else getHeadColumn quilt
    :: rowsToColumns (getTailColumn quilt)
  end
  fun revColumns [] = [] | revColumns quilt =
  let
    fun reverse [] = [] | reverse lst = reverse (tl lst) @ [hd lst]
  in
    reverse (hd quilt) :: revColumns (tl quilt)
  end
  fun rotateSquares quilt = 
  let
    fun metaMap f quilt = map (fn quiltRow => map f quiltRow) quilt
  in
    metaMap rotate quilt
  end
in
rotateSquares (revColumns (rowsToColumns quilt))
end;

fun unturn quilt = turn (turn (turn quilt));

fun pile (quilt1,quilt2) = turn (sew (unturn quilt1, unturn quilt2));

fun pinwheel (quilt) = pile (sew (quilt, turn quilt), sew (unturn quilt, turn (turn quilt)));

fun repeat_block (quilt,m,n) = 
let
  fun repeat_row (quilt,1) = quilt
    | repeat_row (quilt,m) = pile (quilt, repeat_row (quilt,m-1))
  fun repeat_column (quilt,1) = quilt
    | repeat_column (quilt,n) = sew (quilt, repeat_column (quilt,n-1))
in
  repeat_row (repeat_column (quilt, n), m)
end;

val a = [[("a",0)]];
val b = [[("b",0)]];

val miniquilt = pile (sew (pinwheel (turn (turn a)), pinwheel (turn (turn (b)))), sew(pinwheel (turn (turn b)), pinwheel (turn (turn a))));

print (quiltToString (repeat_block (miniquilt, 2,5)));