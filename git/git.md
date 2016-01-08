# 設定

- `--global` をつけると、そのPC全体の設定。~/.gitconfig に書かれる。
- つけないとそのリポジトリだけの設定  リポジトリの .git/config に書かれる。

```
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
git config --global push.default simple

# windows でも unix的改行コードが中心なので、以下を設定しておく。
git config --global core.eol lf 
git config --global core.autocrlf false

```

確認 

```
git config --list
```

参考 - <cite>[Git - 最初のGitの構成](https://git-scm.com/book/ja/v1/%E4%BD%BF%E3%81%84%E5%A7%8B%E3%82%81%E3%82%8B-%E6%9C%80%E5%88%9D%E3%81%AEGit%E3%81%AE%E6%A7%8B%E6%88%90 "Git - 最初のGitの構成")</cite>


## メールアドレスを非公開にしてgit,githubで活動する方法

<cite>[Keeping your email address private - User Documentation](https://help.github.com/articles/keeping-your-email-address-private/ "Keeping your email address private - User Documentation")</cite>

- github の Settings > Emails > Keep my email address private. にする。
- git の user.emailの設定を、`<username>@users.noreply.github.com` を使う。



## リポジトリに寄らず効く .gitignore 関係

vimの swap ファイルなどは、リポジトリの .gitignore に入れるより、
その環境として無視設定しておく方がいい。
(誰がどのエディタで編集して、どういう一時ファイルができるかは読み切れないので、
リポジトリではなく編集する人の側で責任を持つ)

~/.gitconfig

```
[core]
	excludesfile = ~/.gitignore
```

~/.gitignore

```
*.sw?
```



# 典型的な開発のときのコマンド

TODO

# add, commit 関係

```
git add ファイル名...    # ファイル指定で add

git add -u    # 既に管理対象、かつ、変更があったファイルをaddする。
```

# diff

```
git diff   # index に add していないモノを表示 (index->WorkTree)
git diff --cached    # 次の commit で反映される変更を表示 ( HEAD->index)
git diff HEAD^ HEAD  # 直前の commit による変更を表示
git diff HEAD^ HEAD --stat
```

# ブランチ関係 ( branch, checkout, push, pull, merge )

まずは確認の方法

```
git branch -avv
```

## リモートの別ブランチをチェックアウトする

```
git checkout -b other_branch origin/other_branch

もしくは (要確認)
git branch other_branch origin/other_branch
git checkout other_branch
```

自動で upstream は設定されたはず。(要確認)


## ローカルで新しいブランチを作る

```
git branch 新ブランチ名
git checkout 新ブランチ名
```

## push

編集して、addとか commit とかしたら push する。

最初の一度だけ(upstreamが設定されていないときだけ)、明示的に上げ先の指定が必要。

```
git push --set-upstream origin 新ブランチ名
もしくは
git push -u origin 新ブランチ名
```

`--set-upstream`, `-u` オプションをつけておくと、upstream 設定もされる。

upstreamがされている、されていないの違いは以下で確認できる
```
git branch -avv

されていない
* jikken1 7280884 Add jikken programs.
  master  f465c57 [origin/master] Initial commit
されている
* jikken1                7280884 [origin/jikken1] Add jikken programs.
  master                 f465c57 [origin/master] Initial commit
```

もし、既にpushしてしまって、upstreamの設定だけしたい場合は、

```
git branch --set-upstream-to origin/新ブランチ名
```

## merge, fetch, pull

```
# issue1 の変更 を master にマージする場合。
git checkout master
git merge issue1
```

```
git pull 
```




## ブランチを消す

```
git branch -d 消したいブランチ
```


# ファイル名の変更・移動

```
git mv oldfile newfile   # ファイル名の変更
```



# 以下、未整理。





