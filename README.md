# 更新



# 2021/8/24 

新增了7步预测的图。以window=7，step=7,的LSTM模型

<img src="D:\Gary\Program\MathProject\ExerciseWork2\resource\image\10step predict confirmed.png" alt="10step predict confirmed" style="zoom:24%;" />

<img src="D:\Gary\Program\MathProject\ExerciseWork2\resource\image\10step predict Recovered.png" alt="10step predict Recovered" style="zoom:24%;" />

<img src="D:\Gary\Program\MathProject\ExerciseWork2\resource\image\10step predict deaths.png" alt="10step predict deaths" style="zoom:24%;" />

<img src="D:\Gary\Program\MathProject\ExerciseWork2\resource\image\10step predict.png" alt="10step predict" style="zoom:24%;" />

有考虑过引入三个变量对死亡量建模，但效果不是很好。还是改成单变量时间序列好了。用自己回归自己。



在第二问的模型中，加入了超级多的噪声。也就是Dropout层。故意让神经元失活。因为毕竟没法见过未来的数据，那么对于模型而言，他也不知道这是不是噪声，那他应该学会处理这种情况。训练大概250个epochs。

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20210824005301523.png" alt="image-20210824005301523"  />

需要从未统计的时间之后42天左右。死亡人数会突破至5023620人。

我有个想法是，需要两个LSTM，一个专门负责预测，一个专门整合数据。就是说把预测的数据合理的并进原数据集。

用神经网络预测的便利：

潜在的关系让网络自己去学。

使用LSTM比RNN好训练些。RNN根本记不住。

不使用全连接或者线性模型的原因。因为这些模型都是基于独立性假设的。而对于疫情爆发来说，这显然不是，疫情发展的情况前后是存在因果关系的，是自相关的。所以不考虑自身的影响，很难说的过去。

他妈的、、、

随手一搭的反而是最好的模型...改了之后的反而不行。截个图，之后好画结构了

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20210824012535456.png" alt="image-20210824012535456" style="zoom:33%;" />

这里最后一层一定不能用sigmoid，因为明显看出疫情是还会成增长趋势。而用sigmoid就将它映射至0，1，通过minmax反归一永远不可能预测出更大的值。这里发现3层LSTM，神经元分别为32，64，128，可以得到不错的效果。验证集的MAE在0.16左右。

## 有几个问题：

LSTM层数不能太多。这是RNN的通病。太深了会饱和。如果把它当作人的话，也就是说它脑子已经装不下更多的有用记忆了。

窗口的大小选择。

预测步长的选择。

模型的合理性。

这些都需要一个解释。

传染病模型表现不好。所以SIR模型应该只作为一个定性的指标。可以预测走势，但没法预测疫情的恶劣程度。

还有就是免不了得解释LSTM中的门控制。





上面的图稍微有点画错了。犯了个错，明天重新跑一下。



对于问题一，还是发现单步预测MAE最小，最好。window=7，step=1

