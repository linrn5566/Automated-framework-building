#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


def run_tests(args):
    import pytest

    pytest_args = [
        '-v',
        '--tb=short',
        f'--platform={args.platform}',
        f'--appium-server={args.appium_server}',
        f'--alluredir={BASE_DIR}/reports/allure-results',
        '--clean-alluredir',
    ]

    if args.device_name:
        pytest_args.append(f'--device-name={args.device_name}')
    if args.app_path:
        pytest_args.append(f'--app-path={args.app_path}')
    if args.udid:
        pytest_args.append(f'--udid={args.udid}')
    if args.no_reset:
        pytest_args.append('--no-reset')
    if args.marks:
        pytest_args.extend(['-m', args.marks])
    if args.keyword:
        pytest_args.extend(['-k', args.keyword])
    if args.parallel:
        pytest_args.extend(['-n', str(args.parallel)])
    if args.html:
        pytest_args.append(f'--html={BASE_DIR}/reports/html/mobile_report.html')
        pytest_args.append('--self-contained-html')

    pytest_args.append(args.path or str(BASE_DIR / 'testcases' / 'mobile'))

    print(f"执行命令: pytest {' '.join(pytest_args)}")
    print('=' * 80)
    return pytest.main(pytest_args)


def main():
    parser = argparse.ArgumentParser(description='移动端自动化测试执行脚本')
    parser.add_argument('--platform', default='android', help='移动端平台: android/ios')
    parser.add_argument('--device-name', help='设备名称')
    parser.add_argument('--app-path', help='App 安装包路径')
    parser.add_argument('--udid', help='设备 UDID')
    parser.add_argument('--appium-server', default='http://127.0.0.1:4723', help='Appium Server 地址')
    parser.add_argument('--no-reset', action='store_true', help='保留应用数据')
    parser.add_argument('-m', '--marks', default='mobile', help='标签过滤')
    parser.add_argument('-k', '--keyword', help='关键字过滤')
    parser.add_argument('-p', '--path', help='测试路径')
    parser.add_argument('-n', '--parallel', type=int, help='并发执行进程数')
    parser.add_argument('--html', action='store_true', help='生成HTML报告')
    parser.add_argument('--env', default='test', help='测试环境: dev/test/staging/prod')
    args = parser.parse_args()

    os.environ['TEST_ENV'] = args.env
    print(f"测试环境: {args.env}")
    print('=' * 80)
    sys.exit(run_tests(args))


if __name__ == '__main__':
    main()
