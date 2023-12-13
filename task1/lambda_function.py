import multiprocessing

def handler(input: dict, context: object) -> dict:
  
  resultado = dict()

  # Quantidade de nucleos da maquina
  n_cpu = multiprocessing.cpu_count()

  # uso de memoria
  memoria_cache = input['virtual_memory-cached']
  memoria_buffer = input['virtual_memory-buffers']
  memoria_total = input['virtual_memory-total']

  #trafego de rede
  bytes_enviados = input['net_io_counters_eth0-bytes_sent']
  bytes_recebidos = input['net_io_counters_eth0-bytes_recv']
  
  # Calculo da porcentagem de Rede, Memoria
  percentagem_memoria =  ((memoria_cache + memoria_buffer) * 100) / memoria_total
  # Documentar o tipo de calculo feito para a rede
  porcentagem_rede = (bytes_enviados * 100) / (bytes_enviados + bytes_recebidos) if bytes_enviados + bytes_recebidos > 0 else 0

  #Calculo para cada CPU
  porcentagem_total_cpu = {}
  for i in range(n_cpu):
    porcentagem_total_cpu[i] = input[f'cpu_percent-{i}']

  # Media movel
  def mean(total_utilization):
    result = sum(total_utilization) / len(total_utilization)
    return result
  
  media_movel = {}
  for i in range(n_cpu):
    utilization =  context.env.get(f'utilization-cpu{i}', [])
    utilization.append(porcentagem_total_cpu[i])
    if len(utilization) > 60:
      utilization.pop(0)
    
    media_movel[i] = mean(utilization) 
    context.env[f'utilization-cpu{i}'] = utilization
    

  # retornado os resultados
  resultado['use-memory-percent'] = percentagem_memoria
  resultado['use-net-percent'] = porcentagem_rede

  for i in range(n_cpu):
    # Media movel por CPU
    resultado[f'Avg_cpu-{i}'] = media_movel[i]
  
  return resultado