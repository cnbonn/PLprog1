#!/usr/bin/python

import sys, csv

def init_check():
    '''Opens datafile and creates fileptr to filename.cv '''
    if len(sys.argv) != 2:
        print ("Usage mdc.py datafile.csv")
        sys.exit(1)
    print( "Opening" , sys.argv[1])
    file = open( sys.argv[1])
    file = csv.reader(file)
    file = list(file)
    file.pop(0)

    out = list(sys.argv[1][:-1])
    out[-1] = 'v'
    out = open("".join(out) , 'w')
    return (file, out)

def normalize( data ):
    quant = len( data[0])-2
    summary = []
    data.pop(0)
    for i in range(2,2+quant):
        for j in data :
            summary.append ( j[i])
        huge = max(summary)
        tiny = min(summary)
        for j in data:
            j[i] = (float(j[i])- float(tiny)) / (float(huge) - float(tiny))
    return data, quant

def simulate( data , SamNum , CentNum , quant ):
    '''Data is our data set
    SamNum is the sample we are seeing if we can identify
    CentNum is the amount of diffrent centroids we will produce
    quant is the dimentions of vectorspace we are working in'''

    sample = data.pop(SamNum)

    CentVector = [[] for i in range(CentNum)]
    
    for i in CentVector:
        for j in range(quant+1):
            i.append(0)

    for line in data:
        #incriment learning vector
        CentVector[ int(line[1]) ][0] += 1
        #print(line)
        for i in range(2,quant+2):
            #print( "centvect first offset",line[1], "second offset",i-2, "vector additive",line[i])
            #print (line)
            CentVector[ int(line[1]) ][i-1] += float(line[i])
            #print (CentVector)
        
    for value in CentVector:
        for i in range(1,quant):
            value[i] = value[i]/value[0]
        
    least = [-1,1000000]
    
    for centroid in CentVector:
        dist = 0
        for i in range(1,len(centroid)):
            dist += (sample[i+1]-centroid[i])**2
        if( dist < least[1]):
            least[1] = dist
            least[0] = CentVector.index(centroid)

    print (least)

def main():
    
    file , out  = init_check()
    file, quant = normalize ( file )

    for i in range( 0 , len(file) ):
        simulate( file[:], i , 3, quant)
    print()
    sys.exit()

if __name__ == "__main__":
    main()


