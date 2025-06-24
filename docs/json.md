# EFUファイルの小さな例
```csv
Filename,Size,Date Modified,Date Created,Attributes
"C:\msys64",,133876022280081366,133739602603410395,16
"C:\msys64\autorebase.bat",82,133262362720000000,133739602600000000,32
"C:\msys64\clang64",0,133665511886007850,133665511886007850,16
```

# JSON に変換した例

```json
[
    {
        "Filename": "C:\\msys64",
        "Size": null,
        "Date Modified": 133876022280081366,
        "Date Created": 133739602603410395,
        "Attributes": 16
    },
    {
        "Filename": "C:\\msys64\\autorebase.bat",
        "Size": 82,
        "Date Modified": 133262362720000000,
        "Date Created": 133739602600000000,
        "Attributes": 32
    },
    {
        "Filename": "C:\\msys64\\clang64",
        "Size": 0,
        "Date Modified": 133665511886007850,
        "Date Created": 133665511886007850,
        "Attributes": 16
    }
]
```
