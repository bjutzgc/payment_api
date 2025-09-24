#!/bin/bash
# 超简单的API测试脚本 - 使用curl命令

BASE_URL="http://127.0.0.1:8000"

echo "🚀 开始运行超简单API测试"
echo "=================================================="

# 1. 健康检查
echo "=== 健康检查 ==="
curl -X GET "$BASE_URL/health" | jq .
echo ""

# 2. 获取Token
echo "=== 获取Token ==="
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}')
echo $TOKEN_RESPONSE | jq .
TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.token // empty')
echo "Token: $TOKEN"
echo ""

# 3. 登录测试
echo "=== 登录测试 ==="
curl -X GET "$BASE_URL/api/v1/login?loginType=1&loginId=test123" | jq .
echo ""

# 4. 每日奖励
echo "=== 每日奖励 ==="
curl -X POST "$BASE_URL/api/v1/daily_gift" \
  -H "Content-Type: application/json" \
  -d '{"uid": "123"}' | jq .
echo ""

# 5. 商城信息
echo "=== 商城信息 ==="
curl -X POST "$BASE_URL/api/v1/store/items" \
  -H "Content-Type: application/json" \
  -d '{"uid": "123"}' | jq .
echo ""

# 6. 支付成功（需要token）
if [ ! -z "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
  echo "=== 支付成功 ==="
  curl -X POST "$BASE_URL/api/v1/payment/success" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
      "order_id": "test_order_001",
      "uid": "123",
      "item_id": 1,
      "price": 19.99,
      "currency": "USD",
      "payment_channel": "stripe",
      "payment_method": "card",
      "ip": "127.0.0.1",
      "country": "US",
      "email": "test@example.com"
    }' | jq .
  echo ""

  # 7. 支付失败
  echo "=== 支付失败 ==="
  curl -X POST "$BASE_URL/api/v1/payment/failure" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
      "order_id": "test_order_002",
      "uid": "123",
      "item_id": 1,
      "price": 19.99,
      "currency": "USD",
      "payment_channel": "stripe",
      "payment_method": "card",
      "ip": "127.0.0.1",
      "country": "US",
      "web_pay_error_code": "card_declined"
    }' | jq .
  echo ""
else
  echo "=== 支付成功 ==="
  echo "错误: 没有有效token，跳过测试"
  echo ""
  echo "=== 支付失败 ==="
  echo "错误: 没有有效token，跳过测试"
  echo ""
fi

# 8. 历史订单
echo "=== 历史订单 ==="
curl -X POST "$BASE_URL/api/v1/orders/history" \
  -H "Content-Type: application/json" \
  -d '{"uid": "123"}' | jq .
echo ""

echo "✅ 所有测试完成!"