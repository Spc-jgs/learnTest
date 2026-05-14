# 1. 导入库
import paramiko
import shlex
import argparse


# 2. 定义函数
def filter_remote_log(host, port, username, password, log_path, keyword, lines=500):
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
        _,stdout, stderr = ssh.exec_command(command)

        # 6. 读取结果
        result = stdout.read().decode("utf-8", errors="ignore")
        error = stderr.read().decode("utf-8", errors="ignore")

        if result:
            print(result)
        else:
            print("没有匹配到日志")

        if error:
            print("错误信息：")
            print(error)

    finally:
        # 7. 关闭 SSH 连接
        ssh.close()


# 使用示例：
# python remote_log_filter.py --log-filename sms-customer-boot --keyword info

# 3. 只有直接运行这个文件时才执行
if __name__ == "__main__":

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="连接远程服务器，读取并筛选日志文件")

    # 定义参数
    parser.add_argument("--host", default="192.168.8.162", help="远程服务器 IP 地址（默认 192.168.8.162）")
    parser.add_argument("--port", type=int, default=22, help="SSH 端口（默认 22）")
    parser.add_argument("--username", default="root", help="用户名（默认 root）")
    parser.add_argument("--password", default="tianquxinxi", help="密码（默认 tianquxinxi）")
    parser.add_argument(
        "--log-filename", required=True, help="日志文件路径（必须提供）"
    )
    parser.add_argument("--keyword", required=True, help="搜索关键词（必须提供）")
    parser.add_argument("--lines", type=int, default=500, help="读取行数（默认 500）")

    # 解析命令行参数
    args = parser.parse_args()

    # 方式 2：format() 方法
    log_path = "/usr/local/javaApp/sms/logs/{}/{}.log".format(
        args.log_filename, args.log_filename
    )
    # f_string 方式
    log_path = (
        f"/usr/local/javaApp/sms/logs/{args.log_filename}/{args.log_filename}.log"
    )

    # 调用函数
    filter_remote_log(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        log_path=log_path,
        keyword=args.keyword,
        lines=args.lines,
    )
