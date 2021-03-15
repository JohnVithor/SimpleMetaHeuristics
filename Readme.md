# GRASP- VNS
Código desenvolvido para a terceira avaliação da Disciplina **IMD1105 – METAHEURÍSTICAS** do Curso de Bacharelado em Tecnologia da Informação da UFRN.

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

```pip install -r src/requirements.txt```


# Rodando algoritmos

Para rodar os algoritmos, utilize o seguinte comando:

```python src\Instancias_TSPlib.py seed tempo processos arquivo_saida.csv```

Onde:
* ```seed``` é a semente para gerar os números pseudo-aleatórios.
* ```tempo``` é o tempo máximo em minutos que um algoritmo pode executar em uma das instâncias.
* ```processos``` é a quantidade de processos que serão criados para executar cada algorimo nas instancias, buscando paralelizar a execução dos mesmo, se possivel.
* ```arquivo_saida``` é o arquivo onde os dados gerados durante a execução serão salvos ao final.




