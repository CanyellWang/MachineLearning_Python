# -*- coding:utf-8 -*-


from pyspark import  SparkContext
myDat=[ [ 1, 3, 4,5 ], [ 2, 3, 5 ], [ 1, 2, 3,4, 5 ], [ 2,3,4, 5 ] ]
sc = SparkContext( 'local', 'pyspark')
myDat=sc.parallelize(myDat) #得到输入数据RDD #myDat.collect(): [[1, 3, 4, 5], [2, 3, 5], [1, 2, 3, 4, 5], [2, 3, 4, 5]]
C1=myDat.flatMap(lambda x: set(x)).distinct().collect() #distinct()是去重操作，对应C1=createC1(myDat) #得到1项集 #[1, 2, 3, 4, 5],
C1=[frozenset([var]) for var in C1] #需要这样做，因为python的代码里需要处理集合操作
D=myDat.map(lambda x: set(x)).collect() #将输入数据RDD转化为set的列表 #[{1, 3, 4, 5}, {2, 3, 5}, {1, 2, 3, 4, 5}, {2, 3, 4, 5}]
D_bc=sc.broadcast(D)
length=len(myDat.collect())
suppData=sc.parallelize(C1).map(lambda x: (x,len([var for var in D_bc.value if x.issubset(var)])/length) if len([var for var in D_bc.value \
        if x.issubset(var)])/length >=0.75 else ()).filter(lambda x: x).collect()
L=[]
L1=[frozenset(var) for var in map(lambda x:x[0],suppData)] #筛选出大于最小支持度
L.append(L1)
k=2
#D_bc=sc.broadcast(D)
while (len(L[k-2])>0):
    Ck=[var1|var2 for index,var1 in enumerate(L[k-2]) for var2 in L[k-2][index+1:] if list(var1)[:k-2]==list(var2)[:k-2]]
    #count_each_ele=myDat.flatMap(lambda x:x).map(lambda x: (x,1)).countByKey()
    #count_each_ele=sc.parallelize(Ck).map(lambda x: filter(lambda y: x.issubset(y),D_bc.value))
    suppData_temp=sc.parallelize(Ck).map(lambda x: (x,len([var for var in D_bc.value if x.issubset(var)])/length) if len([var for var in D_bc.value \
        if x.issubset(var)])/length >=0.75 else ()).filter(lambda x: x).collect()
    #Ck中的多个子集会分布到多个分布的机器的任务中运行，D_bc是D的分发共享变量，在每个任务中，都可以使用D_bc来统计本任务中包含某子集的个数
    suppData+=suppData_temp
    L.append([var[0] for var in suppData_temp]) #使用这行代码，最后跳出while后再过滤一下空的项
    k+=1
L=[var for var in L if var]
print(L)
print(suppData)
def calcConf(freqSet, H, supportData, brl, minConf=0.7 ):
    prunedH=[]
    #sc.parallelize(H).map(lambda x: ...) #这里也无法并行，因为，freqSet是局部的，如果弄成广播，那得好多副本
    for conseq in H:
        conf = supportData[ freqSet ] / supportData[ freqSet - conseq ]
        if conf >= minConf:
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)
            brl.append( ( freqSet - conseq, conseq, conf ) )
            prunedH.append( conseq )
    return prunedH
def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7):
    m=len(H[0])
    if len(freqSet)>m+1:
        Hmp1=[var1|var2 for index,var1 in enumerate(H) for var2 in H[index+1:] if list(var1)[:m+1-2]==list(var2)[:m+1-2]]
        Hmp1 = calcConf( freqSet, Hmp1, supportData, brl, minConf )
        if len( Hmp1 ) > 1:
            rulesFromConseq( freqSet, Hmp1, supportData, brl, minConf )
def generateRules( L, supportData, minConf=0.7 ):
    bigRuleList = []
    for i in range( 1, len( L ) ):
        for freqSet in L[ i ]:
            H1 = [ frozenset( [ item ] ) for item in freqSet ]
            if i > 1:
                rulesFromConseq( freqSet, H1, supportData, bigRuleList, minConf )
            else:
                calcConf( freqSet, H1, supportData, bigRuleList, minConf )
    return bigRuleList
suppData_dict={}
suppData_dict.update(suppData) #查字典类型的update用法
sD_bc=sc.broadcast(suppData_dict)
rules = generateRules( L, sD_bc.value, minConf=0.9 )
print('rules:\n', rules)
