# 1. 导入库
# datetime 是一个标准库，用于处理日期和时间，可以帮助我们生成带有时间戳的文件名，方便保存筛选结果。
from datetime import datetime

# paramiko 是一个第三方库，用于实现 SSH 协议，允许我们在 Python 中连接远程服务器并执行命令。
import paramiko

# shlex 是一个标准库，用于处理 shell 命令行字符串，提供了安全的方式来构建命令，防止命令注入攻击。
import shlex

# json 是一个标准库，用于处理 JSON 数据格式，可以方便地读取和写入 JSON 文件。
import json

# posixpath 是一个标准库，提供了用于处理 POSIX 路径的函数，可以帮助我们构建远程服务器上的文件路径。
import posixpath


# 2. 定义函数
def filter_remote_log(host, port, username, password, log_path, log_filename, keyword, lines=500):
    """
    连接远程服务器，读取指定日志文件的最后 lines 行，并筛选 keyword
    """

    # 1. 创建 SSH 客户端
    ssh = paramiko.SSHClient()

    # 2. 自动信任第一次连接的服务器指纹
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 3. 连接远程服务器
        ssh.connect(
            hostname=host, port=port, username=username, password=password, timeout=10
        )

        # 4. 拼接远程 Linux 命令
        # shlex.quote 是为了防止路径或关键字里有特殊字符
        safe_log_path = shlex.quote(log_path)
        safe_keyword = shlex.quote(keyword)

        command = (
            f"tail -n {lines} {safe_log_path} | grep --color=never -i {safe_keyword}"
        )

        print(f"执行远程命令：{command}")
        print("-" * 80)

        # 5. 执行远程命令
        # 注意：exec_command 返回的是一个三元组 (stdin, stdout, stderr)，我们只需要 stdout 和 stderr, 因为我们不需要向远程命令输入任何内容，所以 stdin 可以忽略掉。
        # stdin, stdout, stderr = ssh.exec_command(command)
        # 也可以直接用 _ 来忽略掉 stdin
        _, stdout, stderr = ssh.exec_command(command)

        # 6. 读取结果
        result = stdout.read().decode("utf-8", errors="ignore")
        error = stderr.read().decode("utf-8", errors="ignore")

        if result:
            save_result(app_name=log_filename, keyword=keyword, content=result)
            print(result)
        else:
            print("没有匹配到日志")

        if error:
            print("错误信息：")
            print(error)

    finally:
        # 7. 关闭 SSH 连接
        ssh.close()


def load_server_config(env, config_path="config.json"):
    """
    根据环境名称读取服务器配置
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if env not in config:
        raise ValueError(f"配置文件中不存在环境：{env}")

    return config[env]


def save_result(app_name, keyword, content):
    """
    将筛选结果保存到本地文件
    """
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"result_{app_name}_{keyword}_{now}.txt"
    
    # 使用 with 语句可以确保文件正确关闭，即使在写入过程中发生错误也能保证资源的释放。
    # with ... as f: 是 Python 中处理文件的推荐方式，它会自动管理文件的打开和关闭，避免忘记关闭文件导致资源泄漏的问题。
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"筛选结果已保存：{filename}")


# 使用示例：
# python remote_log_filter.py --log-filename sms-customer-boot --keyword info

# 3. 只有直接运行这个文件时才执行
if __name__ == "__main__":

    # 还可以写在函数外面，这样在导入这个模块时就会执行一次，加载配置文件并打印出来。
    # 但是如果配置文件很大或者需要频繁读取，可能会影响性能，或者在导入模块时就需要配置文件存在，否则会抛出异常。
    # argparse 是一个标准库，用于解析命令行参数，使得我们可以从命令行传递参数给脚本。
    import argparse

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="连接远程服务器，读取并筛选日志文件")

    # 定义参数
    parser.add_argument("--env", required=True, help="环境名称，例如 test / prod")
    parser.add_argument(
        "--log-filename", required=True, help="日志文件路径（必须提供）"
    )
    parser.add_argument("--keyword", required=True, help="搜索关键词（必须提供）")
    parser.add_argument("--lines", type=int, default=500, help="读取行数（默认 500）")

    # 解析命令行参数
    args = parser.parse_args()

    server_config = load_server_config(args.env)

    # 使用 posixpath.join 来构建远程服务器上的日志文件路径，这样可以避免手动拼接路径时可能出现的错误，例如忘记添加斜杠或者多添加斜杠。
    log_path = posixpath.join(
        server_config["base_path"], args.log_filename, f"{args.log_filename}.log"
    )

    # 调用函数
    filter_remote_log(
        host=server_config["host"],
        port=server_config["port"],
        username=server_config["username"],
        password=server_config["password"],
        log_path=log_path,
        log_filename=args.log_filename,
        keyword=args.keyword,
        lines=args.lines,
    )
