#!/bin/bash

# Payment API 登录接口简化测试脚本

BASE_URL="http://localhost:8000/api/v1"

echo "==== Payment API 登录接口测试 ===="
echo "基础URL: $BASE_URL"
echo ""

# 简单测试函数
test_login() {
    local login_type=$1
    local login_id=$2
    local description=$3
    local extra_params=$4
    
    echo "测试: $description"
    local url="${BASE_URL}/login?login_type=${login_type}&login_id=${login_id}"
    if [ ! -z "$extra_params" ]; then
        url="${url}&${extra_params}"
    fi
    
    echo "URL: $url"
    echo "响应:"
    curl -s "$url" | python3 -m json.tool
    echo ""
    echo "-----------------------------------"
    echo ""
}

# 1. Facebook登录测试
test_login 1 "facebook_test_id_12345" "Facebook登录"

# 2. Google登录测试  
test_login 2 "google_test_id_67890" "Google登录"

# 3. UserToken登录测试（使用测试token）
USER_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NSwidGVzdCI6dHJ1ZSwiaWF0IjoxNjk5OTk5OTk5LCJleHAiOjE3MDAwMDM1OTl9.test_signature"
test_login 3 "dummy_login_id" "UserToken登录" "user_token=${USER_TOKEN}"

# 4. 邮箱登录测试
test_login 4 "test@example.com" "邮箱登录" "login_code=123456"

# 5. SMS登录测试
test_login 5 "+1234567890" "SMS登录" "login_code=654321"

# 6. Apple登录测试
test_login 6 "apple_test_id_99999" "Apple登录"

echo "==== 错误参数测试 ===="
echo ""

# 测试无效登录类型
echo "测试: 无效登录类型 (99)"
curl -s "${BASE_URL}/login?login_type=99&login_id=test" | python3 -m json.tool
echo ""

# 测试UserToken登录缺少user_token
echo "测试: UserToken登录缺少user_token参数"
curl -s "${BASE_URL}/login?login_type=3&login_id=test" | python3 -m json.tool
echo ""

# 测试邮箱登录缺少验证码
echo "测试: 邮箱登录缺少验证码"
curl -s "${BASE_URL}/login?login_type=4&login_id=test@example.com" | python3 -m json.tool
echo ""

echo "==== 测试完成 ===="