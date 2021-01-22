========
NTFS
========

NTFSの構造を見る
==============================

`Active@ Disk Editor <https://www.disk-editor.org/index.html>`_ というソフトが便利。

使い方の例

- 【図解】NTFSファイルシステムの仕組みと構造解析～MFT, 拡張属性, 代替データストリーム～ | SEの道標

  - https://milestone-of-se.nesuke.com/sv-basic/windows-basic/ntfs-filesystem-structure/


NTFS の拡張属性とは
=======================

(例) WSL1で、metadata を有効にした場合のパーミッションは、ここの拡張領域というところに入っている。

- https://docs.microsoft.com/ja-jp/windows/wsl/file-permissions


.. image:: ../img/NTFS_EA.png

構造

- https://docs.microsoft.com/ja-jp/windows-hardware/drivers/ddi/wdm/ns-wdm-_file_full_ea_information
- https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/0eb94f48-6aac-41df-a878-79f4dcfd8989

::

    typedef struct _FILE_FULL_EA_INFORMATION {
      ULONG  NextEntryOffset;
      UCHAR  Flags;
      UCHAR  EaNameLength;
      USHORT EaValueLength;
      CHAR   EaName[1];
    } FILE_FULL_EA_INFORMATION, *PFILE_FULL_EA_INFORMATION;

- nameの後ろと、valueの後ろに、1バイトずつ0x00が入っている。
- この0x00は EaNameLength,EaValueLength には含まれていない。
- よって、EaValueの先頭位置は、EaName + EaNameLength + 1 になる。

