#!/bin/bash

# Payment API 登录接口 CURL 测试脚本
# 测试所有支持的登录类型

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 基础配置
BASE_URL="http://localhost:8000"
API_BASE="${BASE_URL}/api/v1"

echo -e "${BLUE}==== Payment API 登录接口测试 ====${NC}"
echo -e "${YELLOW}测试基础地址: ${BASE_URL}${NC}"
echo ""

# 检查服务是否启动
echo -e "${YELLOW}1. 检查服务健康状态...${NC}"
curl -s "${BASE_URL}/health" > /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 服务已启动${NC}"
else
    echo -e "${RED}✗ 服务未启动，请先运行: python run.py${NC}"
    exit 1
fi
echo ""

# 测试函数
test_login() {
    local login_type=$1
    local login_id=$2
    local description=$3
    local extra_params=$4
    
    echo -e "${YELLOW}测试 ${description} (login_type=${login_type})...${NC}"
    
    # 构建完整的URL
    local url="${API_BASE}/login?login_type=${login_type}&login_id=${login_id}"
    if [ ! -z "$extra_params" ]; then
        url="${url}&${extra_params}"
    fi
    
    echo -e "${BLUE}请求URL: ${url}${NC}"
    
    # 发送请求并格式化输出
    response=$(curl -s -w "\n%{http_code}" "$url")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    echo -e "${BLUE}HTTP状态码: ${http_code}${NC}"
    echo -e "${BLUE}响应内容:${NC}"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ 请求成功${NC}"
    else
        echo -e "${RED}✗ 请求失败${NC}"
    fi
    echo ""
}

# 测试用户Token登录需要先生成一个有效的token
generate_user_token() {
    echo -e "${YELLOW}生成用户Token用于测试...${NC}"
    
    # 这里使用一个模拟的JWT token，实际环境中应该是有效的
    # 格式: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NSwiaWF0IjoxNjk5OTk5OTk5LCJleHAiOjE3MDAwMDM1OTl9.signature
    
    local header='{"typ":"JWT","alg":"HS256"}'
    local payload='{"user_id":12345,"iat":1699999999,"exp":1700003599}'
    
    # 注意：这是一个示例token，实际测试时需要使用真实的JWT token
    USER_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NSwidGVzdCI6dHJ1ZSwiaWF0IjoxNjk5OTk5OTk5LCJleHAiOjE3MDAwMDM1OTl9.test_signature"
    
    echo -e "${BLUE}生成的测试Token: ${USER_TOKEN:0:50}...${NC}"
    echo ""
}

echo -e "${BLUE}==== 开始登录接口测试 ====${NC}"
echo ""

# 1. Facebook登录测试
test_login 1 "facebook_test_id_12345" "Facebook登录"

# 2. Google登录测试  
test_login 2 "google_test_id_67890" "Google登录"

# 3. UserToken登录测试
generate_user_token
test_login 3 "dummy_login_id" "UserToken登录" "user_token=${USER_TOKEN}"

# 4. 邮箱登录测试
test_login 4 "test@example.com" "邮箱登录" "login_code=123456"

# 5. SMS登录测试
test_login 5 "+1234567890" "SMS登录" "login_code=654321"

# 6. Apple登录测试
test_login 6 "apple_test_id_99999" "Apple登录"

echo -e "${BLUE}==== 参数验证测试 ====${NC}"
echo ""

# 测试无效的登录类型
echo -e "${YELLOW}测试无效登录类型 (login_type=99)...${NC}"
curl -s "${API_BASE}/login?login_type=99&login_id=test" | python3 -m json.tool 2>/dev/null
echo ""

# 测试缺少login_id
echo -e "${YELLOW}测试缺少login_id参数...${NC}"
curl -s "${API_BASE}/login?login_type=1" | python3 -m json.tool 2>/dev/null
echo ""

# 测试UserToken登录缺少user_token
echo -e "${YELLOW}测试UserToken登录缺少user_token参数...${NC}"
curl -s "${API_BASE}/login?login_type=3&login_id=test" | python3 -m json.tool 2>/dev/null
echo ""

# 测试邮箱登录缺少验证码
echo -e "${YELLOW}测试邮箱登录缺少验证码...${NC}"
curl -s "${API_BASE}/login?login_type=4&login_id=test@example.com" | python3 -m json.tool 2>/dev/null
echo ""

echo -e "${BLUE}==== 完整URL示例 ====${NC}"
echo ""
echo -e "${GREEN}Facebook登录:${NC}"
echo "curl \"${API_BASE}/login?login_type=1&login_id=facebook_test_id_12345\""
echo ""

echo -e "${GREEN}Google登录:${NC}"
echo "curl \"${API_BASE}/login?login_type=2&login_id=google_test_id_67890\""
echo ""

echo -e "${GREEN}UserToken登录:${NC}"
echo "curl \"${API_BASE}/login?login_type=3&login_id=dummy&user_token=YOUR_JWT_TOKEN_HERE\""
echo ""

echo -e "${GREEN}邮箱登录:${NC}"
echo "curl \"${API_BASE}/login?login_type=4&login_id=test@example.com&login_code=123456\""
echo ""

echo -e "${GREEN}SMS登录:${NC}"
echo "curl \"${API_BASE}/login?login_type=5&login_id=+1234567890&login_code=654321\""
echo ""

echo -e "${GREEN}Apple登录:${NC}"
echo "curl \"${API_BASE}/login?login_type=6&login_id=apple_test_id_99999\""
echo ""

echo -e "${BLUE}==== 测试完成 ====${NC}"
echo ""
echo -e "${YELLOW}注意事项:${NC}"
echo "1. 以上测试使用的是示例数据，实际用户可能不存在"
echo "2. UserToken需要使用真实有效的JWT token"
echo "3. 邮箱和SMS登录需要有效的验证码"
echo "4. 确保数据库中有对应的测试用户数据"
echo ""
echo -e "${YELLOW}如需查看API文档，请访问:${NC}"
echo "${BASE_URL}/docs (Swagger UI)"
echo "${BASE_URL}/redoc (ReDoc)"