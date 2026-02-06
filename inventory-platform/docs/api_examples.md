# API examples

## Obtain token from Django portal
```bash
curl -b cookies.txt -c cookies.txt -X POST http://localhost:8000/accounts/login/ -d "username=admin&password=admin123"
curl -b cookies.txt http://localhost:8000/accounts/api/token/
```

## Create branch
```bash
curl -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Branch North","location":"North City","timezone":"UTC"}' \
  http://localhost:8001/v1/branches
```

## Adjust stock
```bash
curl -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"branch_id":1,"item_id":1,"quantity":50}' \
  http://localhost:8001/v1/stock
```

## Create, submit, fulfill order
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"branch_id":1,"lines":[{"item_id":1,"requested_qty":2}]}' \
  http://localhost:8001/v1/orders
curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8001/v1/orders/1/submit
curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8001/v1/orders/1/fulfill
```
