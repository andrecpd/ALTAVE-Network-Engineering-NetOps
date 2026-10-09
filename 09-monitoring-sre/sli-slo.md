# SLI/SLO para infraestrutura de redes

Defina objetivos com base nos requisitos do serviço; os valores abaixo devem ser acordados com as áreas responsáveis, não presumidos.

| Indicador | Definição | Uso |
|---|---|---|
| Disponibilidade do túnel | Tempo em estado operacional / tempo observado | Detectar indisponibilidade |
| RTT | Tempo de ida e volta | Medir latência |
| Perda de pacotes | Pacotes perdidos / enviados | Detectar degradação |
| Jitter | Variação da latência | Avaliar tráfego sensível ao tempo |
| Utilização do link | Tráfego / capacidade disponível | Antecipar saturação |
| MTTR | Tempo médio para restaurar o serviço | Medir resposta a incidentes |
| Taxa de mudanças com falha | Mudanças que geram incidente / total de mudanças | Avaliar qualidade de mudanças |

## Boas práticas

- Medir de pontos de vista distintos, incluindo as unidades remotas.
- Definir limiares com baseline e criticidade de negócio.
- Alertar por impacto no serviço, não apenas por estado de interface.
- Documentar runbooks e responsáveis por escalonamento.
- Testar periodicamente alertas e procedimentos de recuperação.
