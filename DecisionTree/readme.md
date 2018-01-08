
- ID3、C4.5的Python实现，其中C4.5有待完善，后续加入CART。
   *ID3采用信息增益<表示得知特征的信息而使得类Y的信息的不确定度减少的程度>进行特征选择
   *ID4.5采用信息增益率<特征A对训练数据集D的信息增益比gR<D,A>定义为其信息珍贵g(D,A)与训练数据集D关于特征A的值的熵HA(D)之比
   *决策树的生成是递归的构建二叉树的过程，对回归树用平方误差最小化准则，对分类树用基尼指数最小化准则，进行特征选择，生成二叉树
- 依赖
	- NumPy
	- Matplotlib


- 测试

		from id3_c45 import DecisionTree
		if __name__=='__main__':
		    #Toy data
		    X = [[1, 2, 0, 1, 0],
		         [0, 1, 1, 0, 1],
		         [1, 0, 0, 0, 1],
		         [2, 1, 1, 0, 1],
		         [1, 1, 0, 1, 1]]
		    y = ['yes','yes','no','no','no']
		  
		    clf = DecisionTree(mode='ID3')
		    clf.fit(X,y)
		    clf.show()
		    print  clf.predict(X)   #['yes' 'yes' 'no' 'no' 'no']
		
		    clf_ = DecisionTree(mode='C4.5')
		    clf_.fit(X,y).show()
		    print clf_.predict(X)   #['yes' 'yes' 'no' 'no' 'no']

	**ID3：**

	![](http://i.imgur.com/kqA3eHT.png)

	**C4.5：**

	![](http://i.imgur.com/ronxb97.png)


- 存在的问题

	(1) 如果测试集中某个样本的某个特征的值在训练集中没出现，则会造成训练出来的树的某个分支，对该样本不能分类，出现KeyError：

		
	    from sklearn.datasets import load_digits
	    dataset = load_digits()
	    X =  dataset['data']
	    y = dataset['target']
	    clf.fit(X[0:1000],y[0:1000])
	    for i in range(1000,1500):
	        try:
	            print clf.predict(X[i])==y[i]
	        except KeyError:
	            print "KeyError"

	(2)目前还不能对多个样本并行预测
