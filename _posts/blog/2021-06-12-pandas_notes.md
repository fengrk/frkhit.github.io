---
layout: post 
title: pandas 备忘 
category: 技术 
tags:
  - pandas 
keywords:
description:
---

# pandas 备忘 

## 1. 读写文件

```python

def read_excel(excel_file: str, only_one_sheet: bool) -> pd.DataFrame:
    kwargs = {}
    if not only_one_sheet:
        kwargs["sheet_name"] = None
    if excel_file.split('.')[-1] in {"xlsx", "xls"}:
        return pd.read_excel(excel_file, **kwargs)
    else:
        return pd.read_csv(excel_file, **kwargs)

```

写文件:

```python

data_list = [
    ("标题 1", "类别 A"),
    ("标题 2", "类别 B"),
]

columns = ["标题", "类别"]
pd.DataFrame(
    data=data_list,
    columns=columns
).to_csv("文件.csv")

```

## 2. 设置单元格格式

需要安装依赖: `python -m pip install xlsxwriter`.

```python


data_list = [
    (0, "标题 1", "类别 A"),
    (1, "标题 2", "类别 B"),
]

columns = ["index", "标题", "类别"]

with pd.ExcelWriter("文件.xlsx") as writer:
    pd.DataFrame(
        data=data_list,
        columns=columns
    ).to_excel(writer, sheet_name="全部", index=False)

    workbook = writer.book
    basic_format = workbook.add_format()
    basic_format.set_font_size(12)
    basic_format.set_align("top")

    title_format = workbook.add_format()
    title_format.set_font_size(12)
    title_format.set_text_wrap()
    title_format.set_align("top")

    class_format = workbook.add_format()
    class_format.set_font_size(12)
    class_format.set_text_wrap()
    class_format.set_align("top")

    for sheet_name, sheet in writer.sheets.items():
        sheet.set_column('A:A', None, basic_format)
        sheet.set_column('B:B', 120, title_format)
        sheet.set_column('C:C', 30, class_format)

```





