#!/bin/bash
set -e

echo "--- Starting Lab 4 Grading (Helm Check) ---"

echo "Step 1: Running helm lint..."
helm lint ./charts/ecommerce-app

echo "Step 2: Checking Production replica count..."
REPLICAS=$(helm template ecommerce ./charts/ecommerce-app -f ./charts/ecommerce-app/values-prod.yaml | grep 'replicas: 3' | xargs)
if [ "$REPLICAS" != "replicas: 3" ]; then
  echo "❌ Error: values-prod.yaml should set replicas to 3."
  exit 1
fi

echo "Step 3: Testing Dry-run installation..."
helm install ecommerce ./charts/ecommerce-app --dry-run --debug

echo "✅ SUCCESS: Lab 4 is passed!"