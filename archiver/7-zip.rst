##########################
7-zip
##########################



============================
コマンドライン
============================



共通スイッチ
=====================

ログ::

    -bb0         ログ出力なし (default)
    -bb1 or -bb  処理されたファイルを出力
    -bb2         show names of additional files that were processed internally in solid archives:
                 skipped files for "Extract" operation, repacked files for 
                 "Add" / "Update" operations.
    -bb3         "Add","Update" 操作に関する追加の操作に関する情報も出力


::

    -bt          Show execution time statistics



圧縮
==================

``a`` 追加。

追加なので、まっさらから作りたかったら一度ファイルを消さないといけない。

::

    # ディレクトリをアーカイブする
    
    7z a c:\Backup\test.7z  "c:\dir1\dir2\dir3"

       指定した dir3 がアーカイブされる。

       中身
           dir3/a.txt
           dir3/b.txt
           ...



- a - Add 。追加になる。
- 出力ファイル拡張子を見て自動で形式を判定。指定する場合は ``-t7z`` など。


除外::

    # 特定のファイルもしくはディレクトリ(直下からのパスで指定)を除外

    7z a c:\Backup\test.7z  "c:\dir1\dir2\dir3" -x!dir3\node_modules

    # 特定の名の付くファイルもしくはディレクトリ(直下だけでなく子孫も含め)を除外

    7z a c:\Backup\test.7z  "c:\dir1\dir2\dir3" -xr!node_modules



TOOD
=====================

(注)フォルダ・ファイルの指定に癖がある。

https://sevenzip.osdn.jp/faq.html の「なぜ「-r」オプションは予想どおりに機能しないのですか？」::

    多くの場合、「-r」オプションは必要ありません。7-Zipは、「-r」オプションがなくてもサブフォルダまで圧縮できます。

    Example 1:
      7z.exe a c:\a.7z "C:\Program Files"

      すべてのサブフォルダも含め、「C:\Program Files」を完全に圧縮します。
      → フルパスでディレクトリを指定した場合、最後の1つのディレクトリ名が prefix になる。

    Example 2:

      7z.exe a -r c:\a.7z "C:\Program Files"

      C:\のサブフォルダ（たとえばC:\WINDOWS）から「Program Files」を検索し、圧縮します。

    もし、なんらかの拡張子の付いたファイルのみを圧縮したい場合は、「-r」オプションを使ってください。

      7z a -r c:\a.zip c:\dir\*.txt 

      c:\dir\フォルダとそのサブフォルダにある、すべての*.txtファイルを圧縮します。


::

    7z a archive1.zip subdir\

        adds all files and subfolders from folder subdir to archive archive1.zip. 
        The filenames in archive will contain subdir\ prefix.

    7z a archive2.zip .\subdir\*

        adds all files and subfolders from folder subdir to archive archive2.zip.
        The filenames in archive will not contain subdir\ prefix.

    cd /D c:\dir1\
    7z a c:\archive3.zip dir2\dir3\ 

        The filenames in archive c:\archive3.zip will contain dir2\dir3\ prefix,
        but they will not contain c:\dir1\ prefix. 
        → 相対パスでディレクトリを指定した場合は、その指定全体がprefixになる。


    7z a Files.7z *.txt -r

        adds all *.txt files from current folder and its subfolders to archive Files.7z.




各引数の末尾の ``\`` 

- つけると ディレクトリ名を指定していることになる
- つけないと、ディレクトリ名 および ファイル名を指定していることになる


