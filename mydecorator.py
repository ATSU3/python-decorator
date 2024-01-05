import json
from flask import request


def pass_json(*keys, **keyvals):
    """JSON形式で受けたリクエストを被修飾関数に適した形にして渡すデコレータ

    keys: 列挙形式で key を指定する。

        [使用例]
        @pass_json("key1", "key2")
        def hello(name, family):

        この場合、"key1", "key2" は各々 "name", "family" と置換され、その結果 JSON は

        {"key1": "Tarou", "key2": "Yamada"} ----> {"name": "Tarou", "family": "Yamada"}

        と変換される。

    keyvals: 辞書形式で key と val を指定する。

        [使用例]
        @pass_json(family="key2")
        def hello(name, family):

       この場合、"key2" が "family" と置換され、その結果 JSON は

        {"name": "Tarou", "key2": "Yamada"} ----> {"name": "Tarou", "family": "Yamada"}

        と変換される。
    """

    def _pass_json(func):
        def wrapper(*args, **kwargs):
            # 被修飾関数 func に渡される引数を初期化
            args_list = list()
            args_dict = dict()

            # この実装では keys と keyvals の併用はできないものとする。
            # もし両者が同時に設定された場合は keys による設定のみが有効となる。
            # また、両者共に設定されない場合は、結果的に request.json がそのまま func に渡されることになる。
            if len(keys) > 0:
                # keys が設定された場合
                # request.json から、各 key に紐付いた value を取り出し、リスト化する。
                for key in keys:
                    args_list.append(request.json[key])
            else:
                # keys が設定されてない場合は keyvals の方を利用する。
                # まず request.json を単純にクローンする。
                for key in request.json:
                    args_dict[key] = request.json[key]
                # 次に keyvals で指定された key に値を付け替える。
                for key in keyvals:
                    val = keyvals[key]
                    args_dict[key] = args_dict.pop(val)

            # func を呼び出す前に、渡される引数を見てみよう!
            print("args_list = " + str(args_list))
            print("args_dict = " + str(args_dict))

            # func を呼び出す。
            # 第 1 引数は「タプル」形式でなくてはならないため、args_list をタプル化する。
            result = func(*tuple(args_list), **args_dict)

            # ここで func は暗黙的に JSON を返却するものと想定している。
            return json.dumps(result), 200, {"Content-Type": "application/json"}

        # Endpoint 毎に呼び出される wrapper 関数の名前が重複しないように、wrapper の名前を被修飾関数名に変更する。
        wrapper.__name__ = func.__name__

        return wrapper

    return _pass_json
