import json
import dash
from dash import html, Dash, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import redis
import time
import multiprocessing


def load_redis():
  n_cpu = multiprocessing.cpu_count()
  # Conectar-se ao servidor Redis
  redis_client = redis.Redis(host='192.168.121.66', port=6379, db=0)
  data = redis_client.get("lucassacramento-proj3-output").decode('utf-8')
    
  # Metricas do desempenho da maquina
  redis_data = json.loads(data)

  percentagem_memoria = redis_data['use-memory-percent']
  percentagem_rede = redis_data['use-net-percent']

  media_movel = {}
  for i in range(n_cpu):
    media_movel[i] = redis_data[f'Avg_cpu-{i}']

  return percentagem_memoria, percentagem_rede, media_movel 

# Criar a aplicação Dash
app = Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    # Uso de CPU, Memória e Rede
    html.H1("DashBoard - Kael & Lucas", style={'text-align': 'center', 'color': 'black', 'font-family': 'Arial', 'padding': '30px'}),
    html.Div([
      html.H2("Média Móvel da CPU"),
      dcc.Graph(id='Live-update-graph'),
      html.H3("Uso de Memória"),
      dcc.Graph(id='memory-graph'),
      html.H3("Uso de Rede"),
      dcc.Graph(id='net-graph')
    ]),
    dcc.Interval(
        id='interval-resources',
        interval=1*1000,  # Atualiza a cada 1 segundos
        n_intervals=0
    )

])

# Atualiza os gráficos com base nos dados do Redis
@app.callback(
    [
      Output('Live-update-graph', 'figure'),
      Output('memory-graph', 'figure'),
      Output('net-graph', 'figure')
    ],
    [Input('interval-resources', 'n_intervals')]
)
def update_graphs(n):
      # Obter dados do Redis
      percentagem_memoria, percentagem_rede,  media_movel  = load_redis()
      print(percentagem_rede)
      print(percentagem_memoria)

      # Criar gráfico de uso de CPU
      cpu_graph = go.Figure()

      cpu_graph.add_trace(go.Bar(
          x=list(media_movel.keys()),
          y=list(media_movel.values()),
          marker=dict(
            color='blue',  # Cor dos marcadores
            opacity=0.8,  # Opacidade dos marcadores
            line=dict(width=0.5, color='black')  # Borda dos marcadores
          ),
          name='Uso de CPU',
      ))

      cpu_graph.update_layout(
        title_text='Uso de CPU Médio por Núcleo',
        xaxis_title='Tempo',
        yaxis_title='Porcentagem (%)', 
        yaxis=dict(range=[0,100]),
        showlegend=True,
        template='plotly_dark'
      )


      # Criar gráfico de uso de memória
      memory_graph = {
        'data': [{
          'value': percentagem_memoria,
          'type': 'indicator',
          'mode': "gauge+number",
          'title': {
            'text': "Uso de Memoria(%)"
          },
          'gauge':{
            'axis': {'range': [0, 100]},
            'bar': {'color': 'darkblue'},
            'steps': [
                {'range':[0,25], 'color': 'green'},
                {'range':[25,50], 'color': 'yellow'},
                {'range':[50,75], 'color': 'orange'},
                {'range':[75,100], 'color': 'red'},
                ]
          }
        }],
        'layout': {'title': 'Uso de memória', 'height': 800, 'color': 'red', 'paper_bgcolor': 'lavander'}
      }

      #Criando gráfico de uso de Rede
      net_graph = {
        'data': [{
          'value': percentagem_rede,
          'type': 'indicator',
          'mode': "gauge+number",
          'title': {
            'text': "Uso de Rede(%)"
          },
          'gauge':{
            'axis': {'range': [0, 100]},
            'bar': {'color': 'darkblue'},
            'steps': [
                {'range':[0,25], 'color': 'green'},
                {'range':[25,50], 'color': 'yellow'},
                {'range':[50,75], 'color': 'orange'},
                {'range':[75,100], 'color': 'red'},
                ]
           }
        }],
        'layout': {'title': 'Uso de memória', 'height': 700, 'color': 'red', 'paper_bgcolor': 'lavander'}
      }
    
      return cpu_graph, memory_graph, net_graph



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=32194)
    
