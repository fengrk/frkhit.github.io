# 修复colaboratory中tensorflow的bug

colaboratory是google推出的类似jupyter的一款产品. 免费使用，提供一个gpu，cpu内存约为12GB. 配合google drive, 可方便进行机器学习的练习. 

colaboratory中的python环境自带丰富的包, tensorflow, pandas, numpy等一应俱全. 但在使用的过程中,发现自带的tensorflow,存在一个bug. 通过探索,本文提供一种修复方案.


## 1.bug描述

colaboratory环境:

```
import sys
import tensorflow as tf

print(tf.__version__) #  1.6.0-rc1

print(sys.version) # 3.6.3 (default, Oct  3 2017, 21:45:48) \n[GCC 7.2.0]

```

在colab中使用slim时, 使用以下代码:

```
slim.assign_from_checkpoint_fn(
        pretrained_model_file,
        variables_to_restore,
        ignore_missing_vars=True)

```

当 `pretrained_model_file = "/content/vgg_19.ckpt" # vgg_19.ckpt为pre-trained model的ckpt文件`, 报异常:

```
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-29-b803c1b9c409> in <module>()
     10 
     11 
---> 12 demo()

<ipython-input-29-b803c1b9c409> in demo()
      7             "1000", "--network", "/content/vgg_19.ckpt",
      8             "--checkpoint-iterations", "10", "--checkpoint-output", "/content/tmp-tv-%s.jpg"]
----> 9     neural_style_main(args)
     10 
     11 

/usr/local/lib/python3.6/dist-packages/neural_style_demo/neural_style.py in main(args)
    178         pooling=options.pooling,
    179         print_iterations=options.print_iterations,
--> 180         checkpoint_iterations=options.checkpoint_iterations
    181     ):
    182         output_file = None

/usr/local/lib/python3.6/dist-packages/neural_style_demo/stylize.py in stylize(network, initial, initial_noiseblend, content, styles, preserve_colors, iterations, content_weight, content_weight_blend, style_weight, style_layer_weight_exp, style_blend_weights, tv_weight, learning_rate, beta1, beta2, epsilon, pooling, print_iterations, checkpoint_iterations)
     77                                                     naming="style-{}".format(i),
     78                                                     pretrained_model_file=pretrained_model_file,
---> 79                                                     checkpoint_exclude_scopes=checkpoint_exclude_scopes)
     80 
     81         for index, layer in enumerate(STYLE_LAYERS):

/usr/local/lib/python3.6/dist-packages/neural_style_demo/losses.py in get_style_features(model_name, style_image, image_size, style_layers, naming, pretrained_model_file, checkpoint_exclude_scopes)
     97                 break
     98         if not excluded:
---> 99             variables_to_restore.append(var)
    100 
    101     return assign_from_checkpoint_fn(

/usr/local/lib/python3.6/dist-packages/tensorflow/contrib/framework/python/ops/variables.py in callback(session)
    688     saver = tf_saver.Saver(var_list, reshape=reshape_variables)
    689     def callback(session):
--> 690       saver.restore(session, model_path)
    691     return callback
    692   else:

/usr/local/lib/python3.6/dist-packages/tensorflow/python/training/saver.py in restore(self, sess, save_path)
   1754       raise ValueError("The specified path: %s is a file."
   1755                        " Please specify only the path prefix"
-> 1756                        " to the checkpoint files." % save_path)
   1757     logging.info("Restoring parameters from %s", save_path)
   1758     if context.in_graph_mode():

ValueError: The specified path: /content/vgg_19.ckpt is a file. Please specify only the path prefix to the checkpoint files.


```

*该代码在本地环境中运行正常!*


## 2.bug的引发原因

google检索,发现该问题有人遇到过,但没有提供原因分析及解决方案.

经过一通排查,将注意力放在

```
/usr/local/lib/python3.6/dist-packages/tensorflow/python/training/saver.py in restore(self, sess, save_path)
   1754       raise ValueError("The specified path: %s is a file."
   1755                        " Please specify only the path prefix"
-> 1756                        " to the checkpoint files." % save_path)
   1757     logging.info("Restoring parameters from %s", save_path)
   1758     if context.in_graph_mode():

```

代码段中.


下载[tensorflow源码](https://github.com/tensorflow/tensorflow), 发现master, r1.6分支中的代码均没发现 `Please specify only the path prefix` 字符串.

找到对应的[saver.py](https://raw.githubusercontent.com/tensorflow/tensorflow/r1.6/tensorflow/python/training/saver.py)文件,也没发现上述字符串.

查看save.py文件的git更新历史

```
git log --pretty=oneline tensorflow/python/training/saver.py

```

```
43ecf848478940904e1a2df10df6bfe72163a38d Revert "Add checkpoint file prefix check (#14341)"
3bd65900f67af950797ef89dde0d984e8b2d0d7a Merge commit for internal changes
e9d4d3d06c0fb211f7488f868fefb477f07df4f8 Adding tf_export decorators/calls to TensorFlow functions and constants.
fa1949b2a73759798e24c640ecd2036d623f6858 Merge commit for internal changes
d56883617c07125eb9d488bc73baccaacd55f48b Enable bulk restoration by default.
2a16133061ba3f8fa60c0338cd629f2211f9b17d Add checkpoint file prefix check (#14341)

```

发现该问题是代码更新引起的, 研究代码及[#14341](https://github.com/tensorflow/tensorflow/pull/14341), 得出bug引发的原因:

- 引入新特性, 针对特定的模型,不允许模型恢复的save_path参数为文件名
- 收集反馈后,该特性撤销
- colaboratory中的tensorflow,使用了带新特性的编译包


## 3.bug修复方案

重装tensorflow包,难以针对colab环境编译,存在风险.


暂时发现最优的方案是: 直接替换环境中saver.py文件.

colab中执行如下(建议在笔记新建后,首先执行该操作):


1.更新saver.py文件

```
# 更新saver.py文件
!wget -O /usr/local/lib/python3.6/dist-packages/tensorflow/python/training/saver.py 'https://raw.githubusercontent.com/tensorflow/tensorflow/r1.6/tensorflow/python/training/saver.py'

# 添加追踪标志
# 原来的环境中,numpy的版本为1.14.0
# 更新后, numpy版本为1.14.1
!pip install --upgrade numpy
import numpy as np
np.__version__ # 1.14.0

```

2.重启环境

Ctrl + M 重启环境
 
3.检查是否生效

```

import numpy as np
np.__version__ # 1.14.1

```
当numpy的版本信息更新后, 便能确认环境重启成功.

再执行slim代码便能正常工作.



