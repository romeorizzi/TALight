(*      

Specchio (selezioni nazionali 2002)

Copyright (C) 2002 Paolo Boldi

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2, or (at your option) any
later version.
	
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
	
You should have received a copy of the GNU General Public License along
with this program; see the file COPYING.  If not, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.  

*)

program specchio;


(* Un nodo dell'albero contiene il numero N di figli, il puntatore (ult)
   all'ultimo figlio più a destra, e il puntatore (prec) al fratello di
   sinistra *)
type albero = record
		N: integer;
		ult, prec: ^albero;
	    end;
     palbero = ^albero;

var inp, out: text;
    a: ^albero;


(* Legge un intero albero dal file f e restituisce il puntatore alla radice *)
function leggialb( var f: text ): palbero;
var a, prev, figlio: ^albero;
    i: integer;
begin
	new(a);
	read( f, a^.N );
	prev:=nil;
	for i:=1 to a^.N do
		begin
			figlio:=leggialb( f );
			figlio^.prec:=prev;
			prev:=figlio
		end;
	a^.ult:=prev;
	a^.prec:=nil;
	leggialb:=a
end;

(* Stampa sul file f l'albero puntato da a *)
procedure stampaalb( var f: text; a: palbero );
var figlio: ^albero;
begin
	write( f, a^.N, ' ' );
	figlio:=a^.ult;
	while ( figlio<>nil ) do
		begin
			stampaalb( f, figlio );
			figlio:=figlio^.prec
		end
end;

begin
	assign( inp, 'input.txt' );
	assign( out, 'output.txt' );	
	reset( inp );
	rewrite( out );

	a:=leggialb( inp );
	close( inp );

	stampaalb( out, a );
	writeln( out );
	close( out )
end.

