# SimpleMetaHeuristics
Código desenvolvido para a Disciplina **IMD1105 – METAHEURÍSTICAS** do Curso de Bacharelado em Tecnologia da Informação da UFRN.

Ministrada no semestre 2020.2 pelo professor: *Antonino Alves Feitosa Neto*

# Configurando ambiente
Após instalar o python no sistema, instale o virtualenv:

```pip install virtualenv```

Com o virtualenv instalado crie o ambiente:

```virtualenv nome_da_virtualenv```

Após criar o ambiente, o ative:

(Linux ou macOS)

```source nome_da_virtualenv/bin/activate```

(Windows)

```nome_da_virtualenv\Scripts\activate```

E por fim, instale os pacotes necessários para rodar os algoritmos:

```pip install -r requirements.txt```


# Rodando algoritmos

Para rodar os algoritmos no grafo de teste, utilize o seguinte comando:

```python src/Teste.py```

Para rodar o algoritmo VNS nas n menores intâncias das 30 selecionadas, utilize o seguinte comando:

```python src/RunVNS.py qtd_instancias seed tamanho_vizinhança máximo_iterações máximo_iterações_sem_atualização tempo_máximo processos arquivo_saida.csv```

Exemplo:

```python src/RunVNS.py 17 42 4 500 250 0.1 10 vns.csv```

Para rodar o algoritmo GRASP nas n menores intâncias das 30 selecionadas, utilize o seguinte comando:

```python src/RunGRASP.py qtd_instancias seed tempo processos arquivo_saida.csv```

Exemplo:

```python src/RunGRASP.py 17 42 0.0 3 1000 500 10 0.1 10 grasp.csv```

Para rodar o algoritmo genético nas n menores intâncias das 30 selecionadas, utilize o seguinte comando:

```python src/RunGenetic.py qtd_instancias seed tamanho_torneio taxa_cruzamento taxa_mutação tamanho_população quantidade_epocas tempo processos arquivo_saida.csv```

Exemplo:

```python src/RunGenetic.py 17 42 10 0.8 0.1 500 2500 0.1 10 genetic.csv```

Para automaticamente identificar o melhor algoritmo, dados os arquivos de saida, utilize o seguinte comando:

```python src/RunGetBest.py qtd_instancias arquivo_entrada_1.csv arquivo_entrada_2.csv arquivo_entrada_3.csv arquivo_saida.csv```

Onde:
* ```qtd_instancias``` é a quantidade de instancias que serão avaliadas, partindo da menor instancia.
* ```seed``` é a semente para gerar os números pseudo-aleatórios.
* ```tempo``` é o tempo máximo em minutos que um algoritmo pode executar em uma das instâncias.
* ```processos``` é a quantidade de processos que serão criados para executar cada algorimo nas instancias, buscando paralelizar a execução dos mesmo, se possivel.
* ```arquivo_saida``` é o arquivo onde os dados gerados durante a execução serão salvos ao final.




