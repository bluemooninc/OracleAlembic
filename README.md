# Oracle Alembic
Alembic は SQLAlchemy を使用してリレーショナルデータベースの作成、変更、削除を管理するマイグレーション・ツールです。

Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine. This tutorial will provide a full introduction to the theory and usage of this tool.

ORACLE データベースをプロジェクトで使用することになりマイグレーションツールを探しましたが Ruby on Rails や CakePHP に採用されている様な使いやすいツールが見当たらず、辿り着いたのが Python の代表的な ORM である SQL Alchemy をベースに使用した Alembic というマイグレーションフレームワークです。


本リポジトリでは docker-compose を使用して oracle-container と alembic-container を立ち上げてマイグレーションの実行を行うサンプルを動作させることが出来、最短の学習でプロジェクトに組み入れることが可能となっています。

## 必要な物

- docker for Mac / Windows
- docker 利用に関する簡単な知識
- ORACLE 利用に関する簡単な知識

## 簡単説明

## マイグレーションの使い方

編集は、ローカルPCの共有フォルダから編集します。

```
# ホストPCにある共有フォルダ
/Users/ユーザー名/コンテナフォルダ/yourproject/alembic/versions
```

マイグレーションコマンドの実行は Alembic コンテナに入ってコマンドラインから実行します。

```
# Alembicコンテナに入る
docker exec -it alembic-container bash
# プロジェクトフォルダに移動する
cd /root/yourproject
```

### 新しいマイグレーションを作成する

```
alembic revision -m "create account table"
```
-m はメッセージタイトルです

### 新しいマイグレーションを編集する

マイグレーションを作成で作られたファイルをエディタで開き、upgradeの pass を削除してそこにSQL分もしくはORMスキームを記述します。
upgradeには実行したいSQLを記述し、downgradeには実行したSQLを打ち消すSQLを記述します。

```
def upgrade():
    pass


def downgrade():
    pass
```

|No| ORM スキーム | 説明 |
|:---|:---|:---|
|1|add_column(table_name, column, schema=None) |カラム追加 |
|2|bulk_insert(table, rows, multiinsert=True) |複数レコード追加 |
|3|create_index(index_name, table_name, columns, schema=None, unique=False, **kw) |インデックス作成 |
|4|create_primary_key(constraint_name, table_name, columns, schema=None) |主キー作成 |
|5|create_table(table_name, *columns, **kw) |テーブル作成 |
|6|execute(command) |SQL実行 |
|7|drop_column(column_name, **kw) |カラム削除 |
|8|drop_table(table_name, schema=None, **kw) |テーブル削除 |
|9|drop_index(index_name, **kw) |インデックス削除|

### 編集例

```
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('account')
```


### マイグレーションを実行する
```
alembic upgrade head
```
### マイグレーションを巻き戻す

巻き戻す(-1)と以前の状態に戻ります。そしてさらに戻す(+1)と現在に戻ります。
```
## 一つ前に戻す
alembic downgrade -1
## 一つ後ろに戻す
alembic upgrade +1
```

## Oracle container information

Oracle のコンテナは、 Docker-hub にある以下URLのイメージをPULLして利用します。

https://hub.docker.com/r/sath89/oracle-12c/ 

docker-compose up を実行すれば、コンテナが起動します。以下設定で ORACLE が利用できるようになっています。

```commandline
hostname: localhost
port: 1521
sid: xe
service name: xe
username: system
password: oracle
```

## Start Alembic project

では、Alembic のコンテナに入ってプロジェクトを進めてみます。

```commandline
docker exec -it alembic-container bash
```

### Creating an Environment 

With a basic understanding of what the environment is, we can create one using alembic init. This will create an environment using the “generic” template:

これから新しくマイグレーションを行うために、genericテンプレートを使用してalembicをジェネレートします。

```
$ cd yourproject
$ alembic init alembic
```
Where above, the init command was called to generate a migrations directory called alembic:
```
Creating directory /path/to/yourproject/alembic...done
Creating directory /path/to/yourproject/alembic/versions...done
Generating /path/to/yourproject/alembic.ini...done
Generating /path/to/yourproject/alembic/env.py...done
Generating /path/to/yourproject/alembic/README...done
Generating /path/to/yourproject/alembic/script.py.mako...done
Please edit configuration/connection/logging settings in
'/path/to/yourproject/alembic.ini' before proceeding.
```
Alembic also includes other environment templates. These can be listed out using the list_templates command:

alembicではgeneric以外に multidb, pylons のテンプレートが使用できます。
```
$ alembic list_templates
Available templates:

generic - Generic single-database configuration.
multidb - Rudimentary multi-database configuration.
pylons - Configuration that reads from a Pylons project environment.

Templates are used via the 'init' command, e.g.:

  alembic init --template pylons ./scripts
```

### Editing the .ini File

Alembic placed a file alembic.ini into the current directory. This is a file that the alembic script looks for when invoked. This file can be anywhere, either in the same directory from which the alembic script will normally be invoked, or if in a different directory, can be specified by using the --config option to the alembic runner.

The file generated with the “generic” configuration looks like:

生成されたiniファイルを接続先に合わせて編集します。sqlalchemy.url の行に接続したいDBのドライバ、ユーザーID、パスワード、接続先ドメイン、接続先DB、オプションを SQL Alchemy のフォーマットで指定します。
ここでは　ORACLE の例ですが、 MySQL, Postgres にも対応しています。

```commandline
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# timezone to use when rendering the date
# within the migration file as well as the filename.
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
#truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; this defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path
# version_locations = %(here)s/bar %(here)s/bat alembic/versions

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

# sqlalchemy.url = driver://user:pass@localhost/dbname

######## USAGE : driver://username:password@server/?option(service_name=XXXXXXX)
sqlalchemy.url = oracle+cx_oracle://system:oracle@oracle-container:1521/?service_name=xe

```

### Create a Migration Script

With the environment in place we can create a new revision, using alembic revision:

以下のコマンドで yourproject フォルダで新たしいリビジョンのマイグレーションファイルを生成します。

```commandline
$ alembic revision -m "create account table"
  Generating /root/yourproject/alembic/versions/36de009415a9_create_account_table.py ... done
```

A new file 36de009415a9_create_account_table.py is generated. Looking inside the file:

すると versions フォルダに新しいマイグレーションファイルが生成されます。ファイルの中身は以下のようになっています。

```commandline
"""create account table

Revision ID: 36de009415a9
Revises: 
Create Date: 2018-08-30 12:57:31.236025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36de009415a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

    
```
The file contains some header information, identifiers for the current revision and a “downgrade” revision, an import of basic Alembic directives, and empty upgrade() and downgrade() functions. Our job here is to populate the upgrade() and downgrade() functions with directives that will apply a set of changes to our database. Typically, upgrade() is required while downgrade() is only needed if down-revision capability is desired, though it’s probably a good idea.

Another thing to notice is the down_revision variable. This is how Alembic knows the correct order in which to apply migrations. When we create the next revision, the new file’s down_revision identifier would point to this one:


```commandline
# revision identifiers, used by Alembic.
revision = 'ae1027a6acf'
down_revision = '1975ea83b712'
```

Every time Alembic runs an operation against the versions/ directory, it reads all the files in, and composes a list based on how the down_revision identifiers link together, with the down_revision of None representing the first file. In theory, if a migration environment had thousands of migrations, this could begin to add some latency to startup, but in practice a project should probably prune old migrations anyway (see the section Building an Up to Date Database from Scratch for a description on how to do this, while maintaining the ability to build the current database fully).

We can then add some directives to our script, suppose adding a new table account:
upgrade 

メソッドには、実行したいスキームを記述します。 スキーム一覧は下記リンクにあります。

http://alembic.zzzcomputing.com/en/latest/ops.html?highlight=create_table#alembic.operations.Operations.create_table

|No|  ORM スキーム | 説明 |
|:---|:---|:---|
|1|add_column(table_name, column, schema=None) |カラム追加 |
|2|bulk_insert(table, rows, multiinsert=True) |複数レコード追加 |
|3|create_index(index_name, table_name, columns, schema=None, unique=False, **kw) |インデックス作成 |
|4|create_primary_key(constraint_name, table_name, columns, schema=None) |主キー作成 |
|5|create_table(table_name, *columns, **kw) |テーブル作成 |
|6|execute(command) |SQL実行 |
|7|drop_column(column_name, **kw) |カラム削除 |
|8|drop_table(table_name, schema=None, **kw) |テーブル削除 |
|9|drop_index(index_name, **kw) |インデックス削除|

```commandline
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
   
```

create_table() and drop_table() are Alembic directives. Alembic provides all the basic database migration operations via these directives, which are designed to be as simple and minimalistic as possible; there’s no reliance upon existing table metadata for most of these directives. They draw upon a global “context” that indicates how to get at a database connection (if any; migrations can dump SQL/DDL directives to files as well) in order to invoke the command. This global context is set up, like everything else, in the env.py script.

### Running our First Migration

We now want to run our migration. Assuming our database is totally clean, it’s as yet unversioned. The alembic upgrade command will run upgrade operations, proceeding from the current database revision, in this example None, to the given target revision. We can specify 1975ea83b712 as the revision we’d like to upgrade to, but it’s easier in most cases just to tell it “the most recent”, in this case head:

マイグレーションファイルの記述が終わったら実行します。

```commandline
$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712
```

Wow that rocked! Note that the information we see on the screen is the result of the logging configuration set up in alembic.ini - logging the alembic stream to the console (standard error, specifically).

The process which occurred here included that Alembic first checked if the database had a table called alembic_version, and if not, created it. It looks in this table for the current version, if any, and then calculates the path from this version to the version requested, in this case head, which is known to be 1975ea83b712. It then invokes the upgrade() method in each file to get to the target revision.

### downgrade

実行結果を確認したら、次は巻き戻しをテストします。以下コマンドで一つ前に戻ります。

```commandline
$ alembic downgrade -1
```
DBからテーブルが消えます（1つ前は空だからです）

### upgrade

巻き戻しからもう一度進める事も出来ます。以下コマンドで巻き戻し前の状態に戻ります。

```commandline
$ alembic upgrade +1
```


### Running our Second Migration
Let’s do another one so we have some things to play with. We again create a revision file:

２つ目のマイグレーションを記述してみて下さい。本リポジトリにはサンプルとして yourproject に最初のマイグレーションファイルが置いてあります。
これに対して項目追加を行う例が以下のマイグレーションです。

```commandline
$ alembic revision -m "Add a column"
Generating /path/to/yourapp/alembic/versions/ae1027a6acf_add_a_column.py...
done

```
Let’s edit this file and add a new column to the account table:

```commandline
"""Add a column

Revision ID: ae1027a6acf
Revises: 1975ea83b712
Create Date: 2011-11-08 12:37:36.714947

"""

# revision identifiers, used by Alembic.
revision = 'ae1027a6acf'
down_revision = '1975ea83b712'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')
```
Running again to head:

```
$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf
```
We’ve now added the last_transaction_date column to the database.

如何でしょうか？
慣れたら、docker-compose.yml の volume 設定を実際のプロジェクトのフォルダ名にしてプロジェクトで活用しましょう。
