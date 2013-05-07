import csv;
import argparse;

def nextract(s):
        v2 = "VARCHAR2("
        l = len( v2 )
        ps = s[0:l]
        if ps.upper() != v2:
                v2 = "Number("
                l = len( v2 )
        nsp = s[l:]
        p =  nsp.find( ')')
        nstring = nsp[:p]
        if 0== len(nstring ):
                return -2
        res = int( nstring)
        return res


val4Db = False
genVal = False
bmode = False
val4Db = False
IBO = False
RET = True
needDiff = False



        
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-t','--table', help='Description for foo argument', required=False)
parser.add_argument('-f','--file', help='csv file', required=False, default='W_PERSO_RETURN.CSV')
args = vars(parser.parse_args())

dBname  = args['table']
file    =   args['file']
gensql = ( None != dBname )


if gensql:
    print "CREATE TABLE " + dBname + "(DUMMYCOLUMN CHAR);"  


csvReader = csv.reader(open(file, 'rb'), delimiter=';')
filler_counter = 0
cres1 = ""
cres2 = ""
resl = ""
resf =""
resv = ""
respl = ""
resC = ""
resS = ""
for row in csvReader:
    if row[0] in ["FileFields", "IGNORE", "FIELD NAME", "COLUMN NAME" ]:
        continue 
    dBColN = row[ 0 ]
    if bmode:
        dBColN = row[4]
    dBColN = dBColN.replace( ' ', '_').replace( '-', '_')
    dbType = row[ 2 ]
    dbDefInn = row[3 ]
    dbIsNullInn = row[4]
    cFieldN = dBColN
    lenField = row[ 2 ]

            
    innPos = row[1]
    if not gensql:
            print dBColN + " " + dbType + " " + dbDefInn + " " + dbIsNullInn + " :: " + innPos
    isDBfield = (len( dBColN ) > 0)
    if isDBfield:
        cFieldN =  dBColN   
    flen = -1 #TODO
    if not gensql:
            print "-----------------------"
    if gensql:
        if isDBfield:

            isBlank = False
            defval = dbDefInn
            if dbDefInn in ["Blank", "Blanks", "Mblank"]:
                flen = nextract( dbType )
                defval = "\'" + " " * int(flen ) + "\'"
                isBlank = True
            defval =  defval.strip()
            if "N" == defval or defval.find( '.') > -1:
                defval = "\'" + defval + "\'"

            if 0 == len( defval ) and not isBlank or defval=="n/a":
                defvalO = ""
            else:
                if defval[0] == '\"':
                    defval = defval.replace( '\"', '\'')
                defvalO = " default " + defval;
            nulldecl = ""
            if not( dbIsNullInn  in ["Y", "yes"]):
                nulldecl = " not null " ;
            
            print "ALTER TABLE " + dBname + " ADD " + dBColN + " "+ dbType + defvalO + nulldecl + ";"
    else:
        cname = dBColN
        if bmode:
             flen = int( lenField)   
        else:
                flen = nextract( dbType )
        print cname + " " + dbType
        
        if val4Db:
                resl += "\',\'"
        else:
                if needDiff:
                        print innPos + " -*-*- " + resl
                        diff = int( innPos ) - len( resl ) - 1
                        if diff > 0:
                                resl += "." * diff
        if 1 == flen :
                resl += "x"
        elif 2 == flen:
                resl += "AB"
        else:
                resl += "a"
                for i in range(2, flen):
                        resl += str( i % 10 )
                resl +=  "b"
        

        if dbType[0] == 'N':
                resf += "LPAD( TO_CHAR(" + dBColN + ")," + str(flen) + ",'0')"
        else:
                resf += dBColN
        resf += ','
        resC += "char " + cFieldN + "[" + str(flen ) + "]" + ';'

        if isDBfield:
                resv += ':' +  dBColN +  "<char[" + str( flen + 1) + "]>,"
                resS += "<<" + cFieldN
        respl += '{' + innPos + ',' + str( flen) + "},"
        if "Filler" == cname:
            cname += "_" + str( filler_counter )
            filler_counter+=1
####        cdef = "char "  + cname + "[" + flen + "] "
####        cres1 += cdef + ";"
##        if (isDBfield ):
##            fpos = row[1]
##            cres2 += "{\"" + dBname + "\"," +  fpos + "," + flen + "}" + ","
print resl
print resf
print resv
print respl
if not( gensql ):
    print "--------------------"
    print cres1
    print
    print cres2
    print resC
    print resS
    print resS.replace( "<<", ">>" );
else:
    print "ALTER TABLE " + dBname + " DROP COLUMN DUMMYCOLUMN;"

            
