#!/bin/bash

services=("user-service" "product-service" "order-service" "payment-service" "review-service" "inventory-service")

for service in "${services[@]}"
do
  docker tag $service ulaj/$service:latest
  docker push ulaj/$service:latest
done