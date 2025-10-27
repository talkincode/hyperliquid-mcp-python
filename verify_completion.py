#!/usr/bin/env python3
"""验证所有任务修复的快速检查脚本"""


def check_constants():
    """检查常量文件是否正确创建"""
    from services.constants import (ADDRESS_PREFIX_LEN,
                                    OCO_GROUP_EXISTING_POSITION,
                                    OCO_GROUP_NEW_POSITION,
                                    ORDER_TYPE_LIMIT_GTC)

    assert OCO_GROUP_NEW_POSITION == "normalTpSl", "新仓位分组常量错误"
    assert OCO_GROUP_EXISTING_POSITION == "positionTpSl", "现有仓位分组常量错误"
    assert ADDRESS_PREFIX_LEN == 6, "地址前缀长度常量错误"
    print("✅ 常量检查通过")


def check_validators():
    """检查验证器是否正确工作"""
    from services.validators import (ValidationError, validate_coin,
                                     validate_price, validate_side,
                                     validate_size)

    # 测试正常情况
    validate_coin("BTC")
    assert validate_side("buy") == True
    assert validate_side("sell") == False
    validate_size(0.1)
    validate_price(100.0)

    # 测试错误情况
    try:
        validate_size(0)
        assert False, "应该抛出 ValidationError"
    except ValidationError:
        pass

    try:
        validate_side("long")
        assert False, "应该抛出 ValidationError"
    except ValidationError:
        pass

    print("✅ 验证器检查通过")


def check_imports():
    """检查所有新模块可以正确导入"""
    try:
        from services.constants import OCO_GROUP_NEW_POSITION
        from services.hyperliquid_services import HyperliquidServices
        from services.validators import ValidationError

        print("✅ 导入检查通过")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    return True


def check_hyperliquid_service_imports():
    """检查 HyperliquidServices 是否正确导入常量"""
    import inspect

    from services import hyperliquid_services

    source = inspect.getsource(hyperliquid_services)

    # 检查是否导入了常量
    assert "from .constants import" in source, "未找到常量导入"
    assert "OCO_GROUP_NEW_POSITION" in source, "未使用新仓位分组常量"
    assert "OCO_GROUP_EXISTING_POSITION" in source, "未使用现有仓位分组常量"

    print("✅ HyperliquidServices 常量使用检查通过")


def check_main_validators():
    """检查 main.py 是否正确集成验证器"""
    import inspect

    import main

    source = inspect.getsource(main)

    # 检查是否导入了验证器
    assert "from services.validators import" in source, "未找到验证器导入"
    assert "ValidationError" in source, "未导入 ValidationError"
    assert "validate_order_inputs" in source, "未导入 validate_order_inputs"

    print("✅ main.py 验证器集成检查通过")


def main():
    """运行所有检查"""
    print("\n🔍 开始验证任务完成情况...\n")

    checks = [
        ("模块导入", check_imports),
        ("常量定义", check_constants),
        ("验证器功能", check_validators),
        ("HyperliquidServices 常量使用", check_hyperliquid_service_imports),
        ("main.py 验证器集成", check_main_validators),
    ]

    passed = 0
    failed = 0

    for name, check_func in checks:
        try:
            check_func()
            passed += 1
        except Exception as e:
            print(f"❌ {name} 失败: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"总计: {passed} 通过, {failed} 失败")

    if failed == 0:
        print("\n🎉 所有检查都通过！任务完成！")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个检查失败，请查看上面的错误")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
