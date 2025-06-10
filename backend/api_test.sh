#!/bin/bash
API_URL="http://localhost:8000"
USER_ID="user_1"
PRODUCT_ID="1"

# List of endpoints to test
endpoints=(
  "/products"
  "/products/$PRODUCT_ID"
  "/products/$PRODUCT_ID/display"
  "/products/sort/stockouts"
  "/metadata/products"
  "/users"
  "/users/$USER_ID"
  "/users/$USER_ID/purchases"
  "/users/$USER_ID/cart"
  "/metadata/users"
)

total=0
passed=0
failed=0

function test_endpoint() {
  local endpoint=$1
  local url="$API_URL$endpoint"
  echo "Testing $endpoint ..."
  echo "  URL: $url"
  response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$url")
  body=$(echo "$response" | sed -e 's/HTTPSTATUS:.*//g')
  status=$(echo "$response" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
  
  # Check if jq is installed for JSON validation
  if command -v jq > /dev/null; then
    echo "$body" | jq . > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      json_status="valid JSON"
      result="PASS"
      ((passed++))
    else
      json_status="invalid JSON"
      result="FAIL"
      ((failed++))
    fi
  else
    if [ -n "$body" ]; then
      json_status="non-empty response"
      result="PASS (no jq)"
      ((passed++))
    else
      json_status="empty response"
      result="FAIL"
      ((failed++))
    fi
  fi
  ((total++))
  echo "  Status: $status | $json_status | $result"
  echo
}

echo "--- Fashnary API Automated Test ---"
echo
for endpoint in "${endpoints[@]}"; do
  test_endpoint "$endpoint"
done
echo "--- Test Summary ---"
echo "Total: $total | Passed: $passed | Failed: $failed"

if [ $failed -eq 0 ]; then
  echo "All tests passed!"
else
  echo "$failed test(s) failed."
fi 