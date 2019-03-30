---
layout: post
title: py3.6环境下numpy C扩展出错
category: 技术
tags: python, numpy
keywords: 
description: 
---

# py3.6环境下numpy C扩展出错

# 1.问题
`python3.6+linux+numpy(1.15.4)`编译[science_rcn](https://github.com/vicariousinc/science_rcn), 报错:
```
/home/frkhit/awsmlenv/lib/python3.6/site-packages/numpy/core/include/numpy/__multiarray_api.h:1542:35: error: return-statement with a value, in function re
turning 'void' [-fpermissive]
     #define NUMPY_IMPORT_ARRAY_RETVAL NULL
                                       ^
    /home/frkhit/awsmlenv/lib/python3.6/site-packages/numpy/core/include/numpy/__multiarray_api.h:1547:151: note: in expansion of macro ‘NUMPY_IMPORT_ARRAY_RET
VAL’
     #define import_array() {if (_import_array() < 0) {PyErr_Print(); PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import"); return NUMP
Y_IMPORT_ARRAY_RETVAL; } }
                                                                                                                                                           ^~~~
~~~~~~~~~~~~~~~~~~~~~
    science_rcn/dilation/dilation.cc:31:5: note: in expansion of macro ‘import_array’
         import_array(); // Must be present for NumPy.  Called first after above line.
         ^~~~~~~~~~~~
    error: command 'x86_64-linux-gnu-gcc' failed with exit status 1

```

# 2.解决方法
参考[pandas](https://github.com/pandas-dev/pandas/issues/3872), [numpy: Writing your own ufunc](https://github.com/numpy/numpy/blob/9245def62e4747324be811f2d4f621a04213c131/doc/source/user/c-info.ufunc-tutorial.rst).

将源代码中的
```
/* ==== Initialize the C_test functions ====================== */
extern "C" {
void init_dilation()
{
    (void) Py_InitModule("_dilation", dilationmethods);
    import_array(); // Must be present for NumPy.  Called first after above line.
}
}
```

修改为:

```
/* ==== Initialize the C_test functions ====================== */
/* This initiates the module using the above definitions. */
#if PY_VERSION_HEX >= 0x03000000
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_dilation",
    NULL,
    -1,
    dilationmethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit__dilation(void)
{
    import_array();
    return PyModule_Create(&moduledef);
}
#else
PyMODINIT_FUNC init_dilation(void)
{
    (void) Py_InitModule("_dilation", dilationmethods);
    import_array();
}
#endif
```
重新编译,成功安装package.

