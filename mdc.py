#!/usr/bin/python

import sys, csv, math

def init_check():
    '''Opens datafile and creates fileptr to filename.cv '''
    if len(sys.argv) != 2:
        print ("Usage mdc.py datafile.csv")
        sys.exit(1)

    file = open( sys.argv[1])
    file = csv.reader(file)
    file = list(file)
    
    header = [[],[]]
    header[0] = file.pop(0)
    header[1]=  file.pop(0)  


    out = list(sys.argv[1][:-1])
    out[-1] = 'v'
    
    out = open("".join(out) , 'w')
    #print(file)
    return (file,header ,out)

def normalize( data, quant ):

    summary = []
    
    for i in range(2,2+quant):
        for j in data :
            summary.append ( j[i])
        huge = max(summary)
        tiny = min(summary)
        for j in data:
            j[i] = (float(j[i])- float(tiny)) / (float(huge) - float(tiny))
        for i in range(0,len(summary)):
            summary.pop()
        
    return data

def simulate( data , SamNum , CentNum , quant ):
    '''Data is our data set
    SamNum is the sample we are seeing if we can identify
    CentNum is the amount of diffrent centroids we will produce
    quant is the dimentions of vectorspace we are working in'''

    sample = data.pop(SamNum)

    #creates list for centroid vectors
    CentVector = [[] for i in range(CentNum)]
    
    #creates space for the centroid vectors
    for i in CentVector:
        for j in range(quant+1):
            i.append(0)

    for line in data:
        #increment learning vector quantity
        CentVector[ int(line[1]) ][0] += 1
        #adds values in learning vector to Centroid
        #adds the values 
        for i in range(2,quant+2):
            CentVector[ int(line[1]) ][i-1] += float(line[i])
    
    #print (CentVector)

    #finds the average of the values
    for value in CentVector:
        for i in range(1,quant+1):
            value[i] = value[i]/value[0]
        
    least = [1000000,-1]

   # print (CentVector)

    for j in range(0 , CentNum):
        dist = 0
        dist = calc_dist(sample[2:], CentVector[j][1:])
        if( dist <= least[0]):
            least[0] = dist
            least[1] = j
    
    return ( SamNum, sample[1], least[1] )

def calc_dist( l1 , l2 ):
    '''Calculates the distance between 2 lists as Vectors
    list 1 should be the sample list  
    list 2 should be the Centroid data 
    WILL NUKE LISTS! pass in sliced versions if you need them later '''
    #print( l1 )
    #print( l2 )
    #l1.pop(1)
    for i in range( len(l2) ):
        l1[i] = float(l1[i]) - float(l2[i])
        l1[i] = pow(l1[i], 2)
    #l1[0] = 0
    ret = math.fsum(l1)
    ret = math.sqrt(ret)
    return ret

def output( outfile, results, header, outputdata):
    print (header[0][0])
    outfile.write(header[0][0])
    outfile.write('\n')

    for i in range(1,len(header[0]) ):
        print( "class", header[0][i][:1], ' (', header[0][i][2:], '):', results[i-1][0], "samples, ", results[i-1][1], "% accuracy" )
        outfile.write( "class {} ({}): {} samples, {}  % accuracy\n".format (header[0][i][:1],header[0][i][2:],results[i-1][0],results[i-1][1] ) )
    
    print( "overall: " , results[-1][0], "samples", results[-1][1],"% accuracy")
    outfile.write("overall: {} samples, {}% accuracy\n".format(results[-1][0], results[-1][1] ))
    
    
    for res in outputdata:
        if(int(res[1]) == int(res[2]) ):
            outfile.write("{},{},{}\n".format( res[0],res[1],res[2] ) )
            pass
        else:
            outfile.write("{},{},{},*\n".format( res[0],res[1],res[2] ) )
            pass
        pass

def parse ( data, classes ):
    pars = [[0,0] for i in range( classes+1)]
    

    for i in data:
        pars[ int(i[1]) ][0] +=1
        pars[classes][0] += 1
        if int(i[1]) == int(i[2]):
            pars[ int(i[1]) ][1] += 1 
            pars[classes][1] += 1
    
    
    for j in pars:
        j[1] = 100 * (j[1]/j[0])
    
    return pars

def main():
    
    file,header, out  = init_check()
    
    #number of disparate datapoints each sample has
    params =  len(header[1])-2 

    #Numbers of classes in file
    cent = len(header[0])-1
    file = normalize ( file, params )
    
    result = []

    for i in range( 0 , len(file), 1):
        result.append( simulate( file[:], i , cent, params))
    output( out, parse(result, cent) , header , result)


if __name__ == "__main__":
    main()


