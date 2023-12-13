# TP3 Cloud Computing

Comandos

TASK 1

Criando arquivos pyfile.yaml, outputkey.yaml com o configmap.
```
kubectl create configmap pyfile --from-file pyfile=lambda_function.py --output yaml > pyfile.yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=lucassacramento-proj3-output --output yaml > outputkey.yaml
```

Criando pod.
```
kubectl -n lucassacramento apply -f deployment.yaml
```

Deletando arquivos no namespace se existirem.
```
kubectl delete configmap pyfile
kubectl delete configmap outputkey
```

Logs do pod.
```
kubectl get pods
kubectl logs <name pod>
```

Deletando pod.
```
kubectl delete deploy serverless-redis
```