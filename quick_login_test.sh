#!/bin/bash

# 快速登录测试命令集合

echo "=== Payment API 登录接口快速测试 ==="
echo "基础地址: http://localhost:8000/api/v1"
echo ""

echo "✅ 1. Facebook登录测试："
echo "curl \"http://localhost:8000/api/v1/login?login_type=1&login_id=facebook_test_12345\""
curl -s "http://localhost:8000/api/v1/login?login_type=1&login_id=facebook_test_12345" | python3 -m json.tool
echo ""

echo "✅ 2. Google登录测试："
echo "curl \"http://localhost:8000/api/v1/login?login_type=2&login_id=google_test_67890\""
curl -s "http://localhost:8000/api/v1/login?login_type=2&login_id=google_test_67890" | python3 -m json.tool
echo ""

echo "✅ 3. UserToken登录测试："
echo "curl \"http://localhost:8000/api/v1/login?login_type=3&login_id=dummy&user_token=test_jwt_token\""
curl -s "http://localhost:8000/api/v1/login?login_type=3&login_id=dummy&user_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NSwidGVzdCI6dHJ1ZX0.signature" | python3 -m json.tool
echo ""

echo "✅ 4. 邮箱登录测试："
echo "curl \"http://localhost:8000/api/v1/login?login_type=4&login_id=test@example.com&login_code=123456\""
curl -s "http://localhost:8000/api/v1/login?login_type=4&login_id=test@example.com&login_code=123456" | python3 -m json.tool
echo ""

echo "✅ 5. SMS登录测试："
echo "curl \"http://localhost:8000/api/v1/login?login_type=5&login_id=+86138888888&login_code=666666\""
curl -s "http://localhost:8000/api/v1/login?login_type=5&login_id=+86138888888&login_code=666666" | python3 -m json.tool
echo ""

echo "✅ 6. Apple登录测试："
echo "curl \"http://localhost:8000/api/v1/login?login_type=6&login_id=apple_test_99999\""
curl -s "http://localhost:8000/api/v1/login?login_type=6&login_id=apple_test_99999" | python3 -m json.tool
echo ""

echo "❌ 7. 错误参数测试："
echo "curl \"http://localhost:8000/api/v1/login?login_type=99&login_id=invalid\""
curl -s "http://localhost:8000/api/v1/login?login_type=99&login_id=invalid" | python3 -m json.tool
echo ""

echo "❌ 8. UserToken缺少token参数："
echo "curl \"http://localhost:8000/api/v1/login?login_type=3&login_id=test\""
curl -s "http://localhost:8000/api/v1/login?login_type=3&login_id=test" | python3 -m json.tool
echo ""

echo "=== 测试结果说明 ==="
echo "• status_code=1: 登录成功"
echo "• status_code=0: 登录失败"
echo "• msg='用户不存在': 数据库中没有对应的测试用户"
echo "• msg='无效的登录参数': 参数验证失败"
echo ""
echo "如需查看完整API文档: http://localhost:8000/docs"